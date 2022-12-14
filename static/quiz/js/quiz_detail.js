console.log('quiz_website')
const url = window.location.href

const quizBox = document.getElementById('quiz_box')


$.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function (response){
        const data = response.data
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)){
                quizBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `
                answers.forEach(answer => {
                    quizBox.innerHTML += `
                        <div class="form-check"> 
                            <input type="checkbox" class="form-check-input" id="${question}-${answer}" name="${question}" value="${answer}">
                            <label for="${question}">${answer}</label>
                        </div>
                    `
                })
            }
        });
    },
    error: function (error){
        console.log(error)
    }
})

const quizForm = document.getElementById('quiz_form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const sendData = () => {
    const elements = [...document.getElementsByClassName('form-check-input')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el => {
        if (el.checked )  {
            data[el.name] += el.value + ', '
        } else {
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
    })

    $.ajax({
        type: 'POST',
        url:`${url}save`,
        data: data,
        success: function (response){
            console.log(response)
        },
        error: function (error){
            console.log(error)
        }
    })
}

quizForm.addEventListener('submit', e => {
    e.preventDefault()

    sendData()
})

