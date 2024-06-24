window.addEventListener('DOMContentLoaded', () => {

    const estateStatusBtns = document.querySelectorAll('button[id^="estateChangeStatusBtn"]');
    estateStatusBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const estateId = e.target.id.split('_').at(-1);
            fetch('http://127.0.0.1:5000/estates', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    estate_id: estateId,
                })
            }).then((response) => {
                return response.json();
            }).then((response) => {
                alert(response);
                var selectedStatus = document.querySelector(`#estateStatus_${estateId}`);
                selectedStatus.disabled = true;
            });
        });
    });

    const advStatusBtns = document.querySelectorAll('button[id^="advChangeStatusBtn');
    advStatusBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const advId = e.target.id.split('_').at(-1);
            fetch('http://127.0.0.1:5000/advertisements', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    advert_id: advId,
                    method: 'change'
                })
            }).then((response) => {
                return response.json();
            }).then((response) => {
                alert(response);
                var selectedStatus = document.querySelector(`#advStatus_${advId}`);
                selectedStatus.disabled = true;
            });
        });
    });

    const advBuyBtns = document.querySelectorAll('button[id^="advBuyBtn_"]');
    advBuyBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const advId = e.target.id.split('_').at(-1);
            const selectedStatus = document.querySelector(`#advStatus_${advId}`);
            if (!selectedStatus.disabled) {
                fetch('http://127.0.0.1:5000/advertisements', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        advert_id: advId,
                        method: 'buy'
                    })
                }).then(response => {
                    return response.json()
                }).then(response => {
                    alert(response)
                });
            } else {
                alert("Вы не можете купить этот лот так, как он закрыт!")
            }
        });
    });

    const regForm = document.querySelector('#regForm');
    regForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const form = new FormData(this);
        fetch('http://127.0.0.1:5000/signup', {
            method: 'POST',
            body: form
        }).then((response) => {
            if (response.status === 201) {
                regForm.childNodes.forEach((node) => {
                    node.disabled = true;
                })
            }
            return response.json();

        }).then((response) => {
            const key = document.querySelector('#public-key');
            const btn = document.querySelector('#reg-continue');
            if (key.lastChild.nodeType === Node.TEXT_NODE) {
                key.removeChild(key.lastChild);
            }
            key.classList.remove('hidden');
            btn.classList.remove('hidden');
            const text = document.createTextNode(response);
            key.appendChild(text);
        });
    });

    const authForm = document.querySelector('#authForm');
    authForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const form = new FormData(this);
        fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            body: form
        }).then((response) => {
            return response.json();
        }).then((response) => {
            const message = document.querySelector('#message');
            if (key.lastChild.nodeName === Node.TEXT_NODE) {
                message.removeChild(message.lastChild);
            }
            message.classList.remove('hidden');
            const text = document.createTextNode(response);
            message.appendChild(text);
        })
    });


})





