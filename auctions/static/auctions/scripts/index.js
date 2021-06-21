function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addToWatchList(button){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "" , false);
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    article_id = button.value;
    button.classList.toggle("add__button--check")
    data = new FormData();
    data.append('pk', article_id)
    xhr.send(data)

}