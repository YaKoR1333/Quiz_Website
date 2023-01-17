console.log('quiz_website')
const url = window.location.href

const quizBox = document.getElementById('quiz_box')
const scoreBOX = document.getElementById('score-box')
const resultBOX = document.getElementById('result-box')

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
        if (!data.hasOwnProperty(el.name)) {
            data[el.name] = ''
        }
        if (el.checked) {
            data[el.name] += el.value + ','
        }
    })

    $.ajax({
        type: 'POST',
        url:`${url}save`,
        data: data,
        success: function (response){
            const results = response.results
            quizForm.classList.add('d-none')

            scoreBOX.innerHTML = `процент правильных ответов: ${response.score.toFixed(2)} %`

            results.forEach(res => {
                const resDiv = document.createElement('div')
                for (const [question, resp] of Object.entries(res)){
                    resDiv.innerHTML += question
                    const cls = ['mt-3', 'mb-3']
                    resDiv.classList.add(...cls)

                    if (resp == 'not answered') {
                        resDiv.innerHTML += '- нет ответа'
                        resDiv.classList.add('text-danger')
                    }
                    else {
                        const answer = resp['answered']
                        const correct = resp['correct_answers']

                        if (JSON.stringify(answer) == JSON.stringify(correct)) {
                            resDiv.classList.add('text-success')
                            resDiv.innerHTML += `Ваш ответ: ${answer}`
                        } else {
                            resDiv.classList.add('text-danger')
                            resDiv.innerHTML += ` | правильный ответ: ${correct}`
                            resDiv.innerHTML += ` | Ваш ответ: ${answer}`
                        }
                    }
                }
                resultBOX.append(resDiv)
            })
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

