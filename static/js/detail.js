let addBtn = document.getElementById('addBtn')

if (true){
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
			var myModal = new bootstrap.Modal(document.getElementById('successModal'), {
				keyboard: false
				})
			console.log('okey')
			myModal.show()
		})
	})
}