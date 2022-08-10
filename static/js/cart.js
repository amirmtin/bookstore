let addBtn = document.getElementById('addBtn')

if (addBtn){
	addBtn.addEventListener('click', (e) => {
		let slug = e.target.getAttribute('book')
		fetch('/api/cart', {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({'book': slug})
		})

		.then(response => response.json())
		.then (result => {
			let message = result.message
			console.log(message)
			var myModal = new bootstrap.Modal(document.getElementById('successModal'), {
				keyboard: false
				})
			myModal.show()
		})
	})
}