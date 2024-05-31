const serverHost = 'http://127.0.0.1:8000'

const field = {
  columns: 7,
  count: 35,
  map: {
    '17': 'cross',
    '9': 'oval'
  }
}

function serializeForm(formNode) {
  const { elements } = formNode

  const data = Array.from(elements)
    .filter((item) => !!item.name)
    .map((element) => {
      const { name, type } = element
      const value = type === 'checkbox' ? element.checked : element.value

      return { name, value }
    })

  return data
}

async function sendData(x, y, field) {
  return await fetch(`${serverHost}/cross/${x}/${y}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: 'field',
  })
    .then(async (r) => {
      if (r.status === 200) {
        onSuccess(await r.json())
      } else {
        onError(await r.json())
      }
      
    })
}

function onSuccess(data) {
  console.log(data)
  console.log('Ваш ход отправлен!')
}

function onError(data) {
  console.log(data)
  console.error('Не удалось отправить ход!')
}

const checkedCells = Object.keys(field.map).map((k) => Number(k))

const form = document.querySelector('.form')
form.addEventListener('submit', async (event) => {
  event.preventDefault()
  const turnData = event.target.getAttribute('data-turn')
  const data = serializeForm(event.target)
    .filter((c) => c.value === true)
    .filter((c) => c.name === turnData)
  await sendData(3, 5, data)
  document.querySelector(`input[name='${turnData}']`).disabled = true
})

const map = document.querySelector('.field')
map.setAttribute('style', `grid-template-columns: repeat(${field.columns}, min-content);`)

for (let i = 0; i < field.count; i++) {
  const label = document.createElement('label')
  label.classList.add('sign')

  const row = Math.floor((i + 1) / field.columns)
  const col = i - row * field.columns
  const checkbox = document.createElement('input')
  checkbox.setAttribute('type', 'checkbox')
  checkbox.setAttribute('name', `cell-${col < 0 ? row - 1 : row}-${col < 0 ? field.columns - 1 : col}`)
  checkbox.classList.add('cell')
  if (checkedCells.includes(i)) {
    checkbox.classList.add(`cell--${field.map[String(i)]}`)
    checkbox.checked = true
    checkbox.disabled = true
  } else {
    checkbox.classList.add('cell--empty')
  }
  checkbox.addEventListener('click', (event) => {
    event.target.classList.add('cell--cross')
    form.setAttribute('data-turn', event.target.name)
    form.dispatchEvent(new Event('submit'))
  })
  
  label.appendChild(checkbox)
  map.appendChild(label)
}