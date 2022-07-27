document.addEventListener('DOMContentLoaded', function() {
});

function update_follower (user_id) {
    fetch(`/user/${user_id}`, {
        method: 'PUT'
    })
    .then(response => response.json())
    .then(result => {
        if (result.followed === true) {
            document.getElementById("follow").style.display = "none";
            document.getElementById("unfollow").style.display = "block";
            number_of_followers = parseInt(document.querySelector("#numbers_followed").innerHTML);
            number_of_followers++
            document.querySelector("#numbers_followed").innerHTML = number_of_followers;
        } else {
            document.getElementById("follow").style.display = "block";
            document.getElementById("unfollow").style.display = "none";
            number_of_followers = parseInt(document.querySelector("#numbers_followed").innerHTML);
            number_of_followers--
            document.querySelector("#numbers_followed").innerHTML = number_of_followers;
        }
    })
}

function like (post_id) {
    fetch(`/like/${post_id}`)
    .then(response => response.json())
    .then(result => {
        if (result.like === true) {
            document.getElementById(`${post_id}`).className = "btn btn-danger";
            like_count = parseInt(document.querySelector(`#like_count${post_id}`).innerHTML);
            like_count ++
            document.querySelector(`#like_count${post_id}`).innerHTML = like_count;
        } else {
            document.getElementById(`${post_id}`).className = "btn btn-outline-danger";
            like_count = parseInt(document.querySelector(`#like_count${post_id}`).innerHTML);
            like_count--
            document.querySelector(`#like_count${post_id}`).innerHTML = like_count;
        }
    })
}

function edit (post_id) {
    old_post = document.querySelector(`#edit${post_id}`).innerHTML
    document.querySelector(`#edit${post_id}`).innerHTML = "Test";
}