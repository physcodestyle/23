const serverHost = 'http://127.0.0.1:8000'

let field = {
  columns: 0,
  count: 0,
  map: {}
}

function buildFieldObject(fieldMatrix) {
  const cross = []
  const oval = []
  let columns = fieldMatrix[0].length
  let count = 0
  for (let i = 0; i < fieldMatrix.length; i++) {
    for (let j = 0; j < fieldMatrix[i].length; j++) {
      count++
      if (fieldMatrix[i][j] === null) {
      } else if (fieldMatrix[i][j]) {
        cross.push(columns * i + j)
      } else {
        oval.push(columns * i + j)
      }
    }
  }
  const map = []
  const preparedCross = cross.reduce((r, c) => { return {...r, [c]: 'cross'} }, {})
  const preparedOval = oval.reduce((r, o) => { return {...r, [o]: 'oval'} }, {})
  Object.keys(preparedCross).forEach((k) => map[k] = preparedCross[k])
  Object.keys(preparedOval).forEach((k) => map[k] = preparedOval[k])
  return {
    columns,
    count,
    map,
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

async function sendData(x, y) {
  return await fetch(`${serverHost}/cross/${x}/${y}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
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
  if (data['turn_result'][0]) {
    field = buildFieldObject(data['turn_result'][1])
    if (data['turn_result'][2]) {
      console.log(data['turn_result'][3])
    }
  }
  setupField()
}

function onError(data) {
  console.log(data)
  console.error('Не удалось отправить ход!')
}

function setupField() {
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
  while (map.firstChild) {
    map.removeChild(map.firstChild)
  }
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
}

fetch(`${serverHost}/game/start`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
})
  .then(async (r) => {
    if (r.status === 200) {
      onSuccess(await r.json())
    } else {
      onError(await r.json())
    }
  })