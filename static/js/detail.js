let addBtn = document.getElementById('addBtn')


addBtn.addEventListener('click', (e) => {
	let slug = e.target.getAttribute('book')
	fetch('/api/cart/', {
		method: 'post',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify({'book': slug})
	})

	.then(response => response.json())
	.then (result => {
		var myModal = new bootstrap.Modal(document.getElementById('successModal'), {
			keyboard: false
			})
		myModal.show()
	})
})

let slug = document.getElementById('addBtn').getAttribute('book')
let submitBtn = document.getElementById('submitRate')

fetch(`/api/rate/?book=${slug}`)
.then(response => response.json())
.then(data => {
	try {
		let rateRadio = document.getElementById(`star${data.rate}`)
		rateRadio.checked = true
	} catch {
		let rateRadio = document.getElementById('star2')
		rateRadio.checked = true
	}
})

submitBtn.addEventListener('click', (e) => {
	let checkedRate = document.querySelector('.rateRadio:checked')
	let rate = parseInt(checkedRate.getAttribute('value'))

	let body = {
		rating: rate,
		book: slug
	}

	fetch('/api/rate/', {
		method: 'post',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify(body)
	})
	.then(response => {
		if (response.status === 200) {
			submitBtn.innerText = 'Submitted!!'
			submitBtn.disabled = true
			setTimeout(() => {
				submitBtn.innerText = 'Submit Rate'
				submitBtn.disabled = false
			}, 1000);
		}
	})
})