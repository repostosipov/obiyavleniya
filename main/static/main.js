console.log('Привет')

const spinnerBox = document.getElementById('spinner-box')
const dataBox = document.getElementById('data-box')

$.ajax({
    type: 'GET',
    url: '/petya/',
    success: function(response){
        setTimeout(()=>{
            spinnerBox.classList.add('d-none')
            for (const item of response){
                dataBox.innerHTML += `
                <div class="row">
                <div class="col-lg-4 col-md-12 mb-1">
                <div class="card">
                <div class="card-body">
                <h4 class="card-title">${item.title}</h4>
                <p class="card-text">${item.content}</p>
                <p class="card-text">
                <strong>${item.created_ad}</strong>
              </p>
              <p class="card-text">На сайте уже
                <strong>${item.created_ad}</strong>
              </p>
                </div></div></div></div>
                
                `
            }
        }, 50)
    },
    error: function(error){
        setTimeout(()=>{
            spinnerBox.classList.add('d-none')
            dataBox.innerHTML = '<p>Какая-то ошибочка</p>'
        }, 500)
    }
})

// ФИЛЬТР ПО ЦЕНЕ

  