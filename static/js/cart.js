let increaseButtons = document.getElementsByClassName('increaseButton')
let deleteButtons   = document.getElementsByClassName('deleteButton')
let decreaseButtons = document.getElementsByClassName('decreaseButton')


for (let i = 0; i < increaseButtons.length; i++) {
	increaseButtons[i].addEventListener('click', (e) => {
		updateOrder(e, +1)
	})
}

for (let i = 0; i < deleteButtons.length; i++) {
	deleteButtons[i].addEventListener('click', event => {
		let book = event.target.getAttribute('data-book')

		let body = {
			'book': book,
		}

		fetch('/api/cart/', {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify(body)
		})
		.then(response => {
			if (response.status === 200) {
				location.reload()
			}
		})
	})
}

for (let i = 0; i < decreaseButtons.length; i++) {
	decreaseButtons[i].addEventListener('click', (e) => {
		updateOrder(e, -1)
	})
}


function updateOrder(event, action) {
	let book = event.target.getAttribute('data-book')

	let body = {
		'book': book,
		'action': action
	}

	fetch('/api/cart/', {
		method: 'put',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify(body)
	})
	.then(response => {
		if (response.status === 200) {
			location.reload()
		}
	})
}