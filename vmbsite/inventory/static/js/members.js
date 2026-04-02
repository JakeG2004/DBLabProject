document.addEventListener('click', function (event) {
    // Determine if we clicked Update or Delete
    const isUpdate = event.target.classList.contains('update-btn');
    const isDelete = event.target.classList.contains('delete-btn');

    if (!isUpdate && !isDelete) return;

    const row = event.target.closest('tr');
    const memberId = row.getAttribute('data-id');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // --- HANDLE DELETE ---
    if (isDelete) {
        if (!confirm("Are you sure?")) return;

        fetch(`/vmb/member/delete/${memberId}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken }
        }).then(response => {
            if (response.ok) row.remove(); // Remove row from UI
        });
    }

    // --- HANDLE UPDATE ---
    if (isUpdate) {
        const firstName = row.querySelector('.first-name').value;
        const lastName = row.querySelector('.last-name').value;

        fetch(`/vmb/member/update/${memberId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                'first_name': firstName,
                'last_name': lastName
            })
        }).then(response => {
            if (response.ok) alert("Member updated!");
        });
    }
});