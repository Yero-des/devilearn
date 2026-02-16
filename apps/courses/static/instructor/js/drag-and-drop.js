const el = document.getElementById('dd-list');
const url = el.dataset.url;
const csrfToken = el.dataset.csrf;

const sortable = Sortable.create(el, {
    animation: 150,
    onEnd: function() {
        const order = Array.from(el.children).map(li => li.dataset.id);
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                order:order,
                moduleId:el.dataset.moduleId
            })        
        }).then(response => {
            if(!response.ok) {
                alert("Error al guardar el nuevo orden")
            }
        })
    }
})