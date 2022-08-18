let increaseButtons = document.getElementsByClassName('increaseButton')
let deleteButtons   = document.getElementsByClassName('deleteButton')
let decreaseButtons = document.getElementsByClassName('decreaseButton')

for (i = 0; i < increaseButtons.length; i++) {
	increaseButtons[i].addEventListener('click', (e) => {
		let slug = e.target.getAttribute('book')

		updateOrder(slug, +1)
	})
}

for (i = 0; i < deleteButtons.length; i++) {
	deleteButtons[i].addEventListener('click', (e) => {
		let slug = e.target.getAttribute('book')

		deleteOrder(slug)
	})
}

for (i = 0; i < decreaseButtons.length; i++) {
	decreaseButtons[i].addEventListener('click', (e) => {
		let slug = e.target.getAttribute('book')

		updateOrder(slug, -1)
	})
}


function updateOrder(book, action) {
	body = {
		'book': book,
		'action': action
	}

	fetch('/api/cart', {
		method: 'put',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify(body)
	})
	.then(response => {
		if (response.status == 200) {
			location.reload()
		}
	})
}

function deleteOrder(book) {
	body = {
		'book': book,
	}

	fetch('/api/cart', {
		method: 'delete',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify(body)
	})
	.then(response => {
		if (response.status == 200) {
			location.reload()
		}
	})
}