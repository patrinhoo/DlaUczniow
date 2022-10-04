from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Course, User, UserProfile, Chapter, Lesson, Requirement, LearnedSkill, Comment, Category
from .forms import ProfileEditForm, RegisterForm, LessonForm


# Create your views here.
class HomeView(TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_courses'] = reversed(
            Course.objects.all().order_by('id')[:12])
        return context


class LoginView(TemplateView):
    template_name = 'base/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_courses'] = Course.objects.all()[:12]
        return context

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        if not username:
            messages.error(request, 'Podaj login!')
            return redirect('login')
        elif not password:
            messages.error(request, 'Podaj hasło!')
            return redirect('login')
        else:
            try:
                user = User.objects.get(username=username)
                user = authenticate(
                    request, username=username, password=password)
                login(request, user)
                return redirect('home')
            except:
                messages.error(request, 'Login lub hasło są niepoprawne!')
                return redirect('login')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class RegisterView(TemplateView):
    template_name = 'base/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_courses'] = Course.objects.all()[:12]
        context['form'] = RegisterForm

        return context

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            user = User.objects.filter(username=username).first()

            UserProfile.objects.create(name=username, user=user)

            messages.success(
                request, 'Pomyślnie utworzono użytkownika ' + username)
            return redirect('login')

        # messages.error(request, 'Nie udało się utworzyć konta')
        messages.error(request, form.errors)
        return redirect('register')


class EditUserView(LoginRequiredMixin, TemplateView):
    template_name = 'base/edit_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = UserProfile.objects.get(user=self.request.user)
        my_courses = Course.objects.filter(author=self.request.user)

        courses = Course.objects.all()
        joined_courses = []

        for course in courses:
            if self.request.user in course.members.all():
                joined_courses.append(course)

        context['profile'] = profile
        context['form'] = ProfileEditForm(instance=profile)
        context['my_courses'] = my_courses
        context['joined_courses'] = joined_courses

        return context

    def post(self, request, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()

        return redirect('edit-user')


class AuthorView(TemplateView):
    template_name = 'base/author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = User.objects.get(id=kwargs['pk'])
        courses = Course.objects.filter(author=author)
        chapters_count = 0
        lessons_count = 0

        for course in courses:
            chapters = Chapter.objects.filter(course=course)
            chapters_count += len(chapters)
            for chapter in chapters:
                lessons = Lesson.objects.filter(chapter=chapter)
                lessons_count += len(lessons)

        context['author'] = author
        context['courses'] = courses
        context['chapters_count'] = chapters_count
        context['lessons_count'] = lessons_count

        return context


class CourseInfoView(TemplateView):
    template_name = 'base/course_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=kwargs['pk'])
        learned_skills = LearnedSkill.objects.filter(course=course)
        requirements = Requirement.objects.filter(course=course)
        chapters = Chapter.objects.filter(course=course)
        lessons_count = 0

        chapters_lessons = dict()
        for chapter in chapters:
            chapter_lessons = Lesson.objects.filter(chapter=chapter)
            chapters_lessons[chapter] = chapter_lessons
            lessons_count += len(chapter_lessons)

        context['course'] = course
        context['learned_skills'] = learned_skills
        context['requirements'] = requirements
        context['chapters_lessons'] = chapters_lessons

        context['chapters_count'] = len(chapters)
        context['lessons_count'] = lessons_count

        return context


class JoinCourseView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            course = Course.objects.get(id=kwargs['pk'])

            chapters = Chapter.objects.filter(course=course)

            chapters_lessons = dict()
            for chapter in chapters:
                chapter_lessons = Lesson.objects.filter(chapter=chapter)
                chapters_lessons[chapter] = chapter_lessons

            active = False
            for chapter, lessons in chapters_lessons.items():
                if lessons:
                    active = True
                    break

            if active:
                if request.user not in course.members.all():
                    print("NIEEEEEEEEEEEEEE")
                    course.members.add(request.user)
                return redirect('course-main', pk=course.id)
            else:
                return redirect('under-construction')
        else:
            messages.error(request, 'Aby dołączyć do kursu zaloguj się!')
            return redirect('login')


class CourseMainView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        course = Course.objects.get(id=kwargs['pk'])
        chapter = Chapter.objects.filter(course=course)[0]
        lesson = Lesson.objects.filter(chapter=chapter)[0]

        return redirect('course', pk=course.id, pk2=lesson.id)


class UnderConstructionView(LoginRequiredMixin, TemplateView):
    template_name = 'base/under_construction.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['recent_courses'] = Course.objects.all()[:12]

        return context


class CourseView(LoginRequiredMixin, TemplateView):
    template_name = 'base/course.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=kwargs['pk'])
        chapters = Chapter.objects.filter(course=course)
        actual_lesson = Lesson.objects.get(id=kwargs['pk2'])
        actual_chapter = actual_lesson.chapter
        comments = Comment.objects.filter(lesson=actual_lesson)[:5]

        chapters_lessons = dict()
        for chapter in chapters:
            chapter_lessons = Lesson.objects.filter(chapter=chapter)
            chapters_lessons[chapter] = chapter_lessons

        context['recent_courses'] = Course.objects.all()[:12]
        context['course'] = course
        context['comments'] = comments
        context['chapters_lessons'] = chapters_lessons
        context['actual_lesson'] = actual_lesson
        context['actual_chapter'] = actual_chapter

        return context

    def post(self, request, *args, **kwargs):
        course = Course.objects.get(id=kwargs['pk'])
        actual_lesson = Lesson.objects.get(id=kwargs['pk2'])

        comment_body = request.POST.get('comment-body')

        if comment_body:
            Comment.objects.create(
                comment_body=comment_body, lesson=actual_lesson, user=self.request.user)
            messages.success(request, 'Pomyślnie dodano komentarz!')
        else:
            messages.error(request, 'Nie udało się dodać komentarza!')

        return redirect('course', pk=course.id, pk2=actual_lesson.id)


class CourseCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'base/course_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['available_categories'] = Category.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        course_name = request.POST.get('course-name')
        category_name = request.POST.get('category')
        description = request.POST.get('description')
        course_image = request.FILES.get('course-image')

        for filename, file in request.FILES.items():
            if file == course_image:
                course_image_name = request.FILES[filename].name

        learned_skills = request.POST.getlist('new-skill')
        requirements = request.POST.getlist('new-requirement')
        chapters = request.POST.getlist('new-chapter')

        if not course_name:
            messages.error(request, 'Podaj nazwę kursu!')
            return redirect('course-create')
        elif len(course_name) > 200:
            messages.error(request, 'Nazwa kursu jest za długa!')
            return redirect('course-create')

        try:
            category = Category.objects.get(category_name=category_name)
        except:
            messages.error(request, 'Musisz wybrać kategorię!')
            return redirect('course-create')

        if not description:
            messages.error(request, 'Brak opisu kursu!')
            return redirect('course-create')

        if course_image and course_image_name.split('.')[-1] in ('jpg', 'png', 'jpeg'):
            course = Course.objects.create(
                course_name=course_name, description=description, author=self.request.user, category=category, image=course_image)
        else:
            course = Course.objects.create(
                course_name=course_name, description=description, author=self.request.user, category=category)

        for skill in learned_skills:
            if skill:
                LearnedSkill.objects.create(skill=skill, course=course)

        for requirement in requirements:
            if requirement:
                Requirement.objects.create(
                    requirement=requirement, course=course)

        for chapter_name in chapters:
            if chapter_name:
                Chapter.objects.create(
                    chapter_name=chapter_name, course=course)

        messages.success(
            request, 'Pomyślnie utworzono kurs: ' + course.course_name)

        return redirect('edit-user')


class CourseEditView(LoginRequiredMixin, TemplateView):
    template_name = 'base/course_edit.html'

    def get(self, request, *args, **kwargs):
        course = Course.objects.get(id=kwargs['pk'])
        if not course.author == request.user:
            messages.error(request, 'Nie jesteś autorem tego kursu!')
            return redirect('edit-user')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=kwargs['pk'])
        actual_category = course.category
        available_categories = Category.objects.exclude(
            category_name=actual_category)

        context['course'] = course
        context['skills'] = LearnedSkill.objects.filter(course=course)
        context['requirements'] = Requirement.objects.filter(course=course)
        context['chapters'] = Chapter.objects.filter(course=course)
        context['actual_category'] = actual_category
        context['available_categories'] = available_categories

        return context

    def post(self, request, *args, **kwargs):
        fine = True
        course = Course.objects.get(id=kwargs['pk'])

        course_name = request.POST.get('course-name')
        category_name = request.POST.get('category')
        description = request.POST.get('description')
        course_image = request.FILES.get('course-image')

        for filename, file in request.FILES.items():
            if file == course_image:
                course_image_name = request.FILES[filename].name

        learned_skills = request.POST.getlist('new-skill')
        requirements = request.POST.getlist('new-requirement')
        chapters = request.POST.getlist('new-chapter')

        if not course_name:
            messages.error(request, 'Podaj nazwę kursu!')
            fine = False
        elif len(course_name) > 200:
            messages.error(request, 'Nazwa kursu jest za długa!')
            fine = False

        try:
            category = Category.objects.get(category_name=category_name)
        except:
            messages.error(request, 'Musisz wybrać kategorię!')
            return redirect('course-create')

        if not description:
            messages.error(request, 'Brak opisu kursu!')
            fine = False

        if course_image and course_image_name.split('.')[-1] in ('jpg', 'png', 'jpeg'):
            course.image = course_image

        course.course_name = course_name
        course.category = category
        course.description = description
        course.save()

        for skill in learned_skills:
            if skill:
                LearnedSkill.objects.create(skill=skill, course=course)

        for requirement in requirements:
            if requirement:
                Requirement.objects.create(
                    requirement=requirement, course=course)

        for chapter_name in chapters:
            if chapter_name:
                Chapter.objects.create(
                    chapter_name=chapter_name, course=course)

        if fine:
            messages.success(
                request, 'Pomyślnie edytowano kurs: ' + course.course_name)
            return redirect('edit-user')
        else:
            return redirect('course-edit', pk=course.id)


class ReqDelView(LoginRequiredMixin, TemplateView):
    template_name = 'base/requirement_del.html'

    def get(self, request, *args, **kwargs):
        requirement = Requirement.objects.get(id=kwargs['pk'])
        if not requirement.course.author == request.user:
            messages.error(request, 'Nie jesteś autorem tego kursu!')
            return redirect('edit-user')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requirement = Requirement.objects.get(id=kwargs['pk'])

        context['requirement'] = requirement

        return context

    def post(self, request, *args, **kwargs):
        try:
            requirement = Requirement.objects.get(id=kwargs['pk'])
            course = requirement.course
            requirement.delete()

            messages.success(request, 'Pomyślnie usunięto wymaganie!')
            return redirect('course-edit', pk=course.id)
        except:
            messages.error(request, 'Nie odnaleziono takiego wymagania!')
            return redirect('course-edit', pk=course.id)


class SkillDelView(LoginRequiredMixin, TemplateView):
    template_name = 'base/skill_del.html'

    def get(self, request, *args, **kwargs):
        skill = LearnedSkill.objects.get(id=kwargs['pk'])
        if not skill.course.author == request.user:
            messages.error(request, 'Nie jesteś autorem tego kursu!')
            return redirect('edit-user')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill = LearnedSkill.objects.get(id=kwargs['pk'])

        context['skill'] = skill

        return context

    def post(self, request, *args, **kwargs):
        try:
            skill = LearnedSkill.objects.get(id=kwargs['pk'])
            course = skill.course
            skill.delete()

            messages.success(
                request, 'Pomyślnie usunięto zdobytą umiejętność!')
            return redirect('course-edit', pk=course.id)
        except:
            messages.error(request, 'Nie odnaleziono takiej umiejętności!')
            return redirect('course-edit', pk=course.id)


class ChapterDelView(LoginRequiredMixin, TemplateView):
    template_name = 'base/chapter_del.html'

    def get(self, request, *args, **kwargs):
        chapter = Chapter.objects.get(id=kwargs['pk'])
        if not chapter.course.author == request.user:
            messages.error(request, 'Nie jesteś autorem tego kursu!')
            return redirect('edit-user')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapter = Chapter.objects.get(id=kwargs['pk'])

        context['chapter'] = chapter

        return context

    def post(self, request, *args, **kwargs):
        try:
            chapter = Chapter.objects.get(id=kwargs['pk'])
            course = chapter.course
            chapter.delete()

            messages.success(
                request, 'Pomyślnie usunięto rozdział!')
            return redirect('course-edit', pk=course.id)
        except:
            messages.error(request, 'Nie odnaleziono takiego rozdziału!')
            return redirect('course-edit', pk=course.id)


class ChapterEditView(LoginRequiredMixin, TemplateView):
    template_name = 'base/chapter_edit.html'

    def get(self, request, *args, **kwargs):
        chapter = Chapter.objects.get(id=kwargs['pk'])
        if not chapter.course.author == request.user:
            messages.error(request, 'Nie jesteś autorem tego kursu!')
            return redirect('edit-user')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapter = Chapter.objects.get(id=kwargs['pk'])
        lessons = Lesson.objects.filter(chapter=chapter)

        context['chapter'] = chapter
        context['lessons'] = lessons

        return context

    def post(self, request, *args, **kwargs):
        fine = True
        chapter = Chapter.objects.get(id=kwargs['pk'])
        course = chapter.course

        chapter_name = request.POST.get('chapter-name')
        new_lessons = request.POST.getlist('new-lesson')
        new_lessons_video = request.FILES.getlist('new-lesson-video')

        print(new_lessons)
        print(new_lessons_video)

        if chapter_name:
            chapter.chapter_name = chapter_name
            chapter.save()

        for name, video in zip(new_lessons, new_lessons_video):
            if not name:
                messages.error(request, 'Nie podano nazwy lekcji!')
                fine = False
            if not video:
                messages.error(request, 'Brak video dla lekcji!')
                fine = False

            if name and video:
                Lesson.objects.create(
                    lesson_name=name, video=video, chapter=chapter)

        if fine:
            messages.success(request, 'Pomyślnie edytowano rozdział!')
            return redirect('course-edit', pk=course.id)
        else:
            return redirect('chapter-edit', pk=chapter.id)


class LessonAddView(LoginRequiredMixin, TemplateView):
    template_name = 'base/lesson_add.html'

    def get(self, request, *args, **kwargs):
        chapter = Chapter.objects.get(id=kwargs['pk'])
        if not chapter.course.author == request.user:
            messages.error(request, 'Nie jesteś autorem tego kursu!')
            return redirect('edit-user')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapter = Chapter.objects.get(id=kwargs['pk'])

        context['chapter'] = chapter
        context['form'] = LessonForm

        return context

    def post(self, request, *args, **kwargs):
        chapter = Chapter.objects.get(id=kwargs['pk'])

        form = LessonForm(request.POST, request.FILES)

        if form.is_valid():
            lesson_name = form.cleaned_data.get('lesson_name')
            video = form.cleaned_data.get('video')
            Lesson.objects.create(lesson_name=lesson_name,
                                  video=video, chapter=chapter)

            messages.success(request, 'Pomyślnie dodano lekcję!')
            return redirect('chapter-edit', pk=chapter.id)

        messages.error(request, 'Nie udało się dodać lekcji!')
        return redirect('lesson-add', pk=chapter.id)


class LessonDelView(LoginRequiredMixin, TemplateView):
    template_name = 'base/lesson_del.html'

    def get(self, request, *args, **kwargs):
        lesson = Lesson.objects.get(id=kwargs['pk'])
        if not lesson.chapter.course.author == request.user:
            messages.error(request, 'Nie jesteś autorem tego kursu!')
            return redirect('edit-user')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = Lesson.objects.get(id=kwargs['pk'])

        context['lesson'] = lesson

        return context

    def post(self, request, *args, **kwargs):
        try:
            lesson = Lesson.objects.get(id=kwargs['pk'])
            chapter = lesson.chapter
            lesson.delete()

            messages.success(
                request, 'Pomyślnie usunięto lekcję!')
            return redirect('chapter-edit', pk=chapter.id)
        except:
            messages.error(request, 'Nie udało się usunąć lekcji!')
            return redirect('lesson-del', pk=lesson.id)


class SearchView(TemplateView):
    template_name = 'base/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = self.request.GET.get(
            'q') if self.request.GET.get('q') != None else ''

        courses = list(Course.objects.filter(course_name__icontains=q))
        by_learned_skills = LearnedSkill.objects.filter(skill__icontains=q)
        by_chapters = Chapter.objects.filter(chapter_name__icontains=q)
        by_category = Category.objects.filter(category_name__icontains=q)
        all_courses = Course.objects.all()

        for skill in by_learned_skills:
            if skill.course not in courses:
                courses.append(skill.course)

        for chapter in by_chapters:
            if chapter.course not in courses:
                courses.append(chapter.course)

        for category in by_category:
            for course in all_courses:
                if course not in courses and course.category == category:
                    courses.append(course)

        context['courses'] = courses

        return context
