const toggleButton = document.getElementsByClassName('toggle-button')[0]
const navbarLinks = document.getElementsByClassName('navbar-links')[0]

toggleButton.addEventListener('click', () => {
    navbarLinks.classList.toggle('active')
})

document.querySelectorAll('.chapter').forEach(chapter => {
    title = chapter.querySelectorAll('.title')[0]
    
    title.addEventListener('click', event => {
        chapter.querySelectorAll('.lesson').forEach(lesson => {
            if (lesson.style.display === "block") {
                lesson.style.display = "none";
            } else {
                lesson.style.display = "block";
            }
        })

        chapter.querySelectorAll('.exercise').forEach(exercise => {
            if (exercise.style.display === "block") {
                exercise.style.display = "none";
            } else {
                exercise.style.display = "block";
            }
        })
    })
})


document.querySelectorAll('.add-skill-button').forEach(button => {
    button.addEventListener('click', event => {
        var div = document.createElement('div');
        div.className = 'skill'
        div.innerHTML = `<input name="new-skill" type="text" value="">
                        <button type="button" class="sub-button">&#8722;</button>`
        parent = button.parentNode

        parent.insertBefore(div, button);

        div.querySelectorAll('.sub-button').forEach(button => {
            button.addEventListener('click', event => {
                button.parentNode.parentNode.removeChild(button.parentNode);
            })
        })
    })
})

document.querySelectorAll('.add-requirement-button').forEach(button => {
    button.addEventListener('click', event => {
        var div = document.createElement('div');
        div.className = 'skill'
        div.innerHTML = `<input name="new-requirement" type="text" value="">
                        <button type="button" class="sub-button">&#8722;</button>`
        parent = button.parentNode

        parent.insertBefore(div, button);

        div.querySelectorAll('.sub-button').forEach(button => {
            button.addEventListener('click', event => {
                button.parentNode.parentNode.removeChild(button.parentNode);
            })
        })
    })
})

document.querySelectorAll('.sub-button').forEach(button => {
    button.addEventListener('click', event => {
        button.parentNode.parentNode.removeChild(button.parentNode);
    })
})

document.querySelectorAll('.sub-lesson-button').forEach(button => {
    button.addEventListener('click', event => {
        button.parentNode.parentNode.parentNode.removeChild(button.parentNode.parentNode);
    })
})

document.querySelectorAll('.add-chapter-button').forEach(button => {
    button.addEventListener('click', event => {
        var div = document.createElement('div');
        div.className = 'course-chapter'
        div.innerHTML = `<input name="new-chapter" type="text" value="">
        <div class="lessons">
            <div class="sub-chapter">
                <button type="button" class="sub-chapter-button">USUŃ ROZDZIAŁ</button>
            </div>
        </div>
        <hr>`

        parent = button.parentNode

        parent.insertBefore(div, button);

        div.querySelectorAll('.sub-chapter-button').forEach(sub_chapter_button => {
            sub_chapter_button.addEventListener('click', event => {
                sub_chapter_button.parentNode.parentNode.parentNode.parentNode.removeChild(sub_chapter_button.parentNode.parentNode.parentNode)
            })
        })
    })
})

document.querySelectorAll('.sub-chapter-button').forEach(button => {
    button.addEventListener('click', event => {
        button.parentNode.parentNode.parentNode.parentNode.removeChild(button.parentNode.parentNode.parentNode)
    })
})
