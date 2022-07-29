document.addEventListener('DOMContentLoaded', function() {
    document.querySelector("#post-message").onkeyup = function () {
        document.querySelector("#post-chars-remaining").innerHTML = `${this.maxLength - this.value.length} characters remaining`;
    }
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
    const old_post = document.querySelector(`#edit${post_id}`).innerHTML.trim();
    document.querySelector(`#edit${post_id}`).innerHTML = `<textarea autofocus class="form-control" id="post-update-msg" name="post-message" required="required" 
    maxlength="280" placeholder="Post">${old_post}</textarea><div class="row m-2" id="edit-chars-remaining">${280-old_post.length} characters remaining</div>`;
    document.querySelector(`#div_edit${post_id}`).style.display = "none";
    const btn_save = `<button id="save" type="button" class="btn btn-outline-primary">Save</button>`;
    const btn_cancel = `<button id="cancel" type="button" class="btn btn-outline-primary">Cancel</button>`;
    document.querySelector(`#buttons${post_id}`).innerHTML = `<div class="btn-group" role="group" aria-label="Basic outlined example">${btn_save}${btn_cancel}</div>`;

    document.querySelector("#post-update-msg").onkeyup = function () {
        console.log(this.maxLength)
        document.querySelector("#edit-chars-remaining").innerHTML = `${this.maxLength - this.value.length} characters remaining`;
    }

    document.querySelector("#save").addEventListener('click', function () {
        const new_post = document.getElementById("post-update-msg").value;
        if (new_post.length > 0) {
            fetch(`/post/${post_id}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({post: new_post})
            })
            .then(response => response.json())
            .then(result => {
                document.querySelector(`#edit${post_id}`).innerHTML = new_post;
                document.querySelector(`#div_edit${post_id}`).style.display = "block";
                document.querySelector(`#buttons${post_id}`).innerHTML = "";
            })
        } else {
            alert("Your needs at least one character.")
        }
        
    })
    document.querySelector("#cancel").addEventListener('click', function () {
        document.querySelector(`#edit${post_id}`).innerHTML = old_post;
        document.querySelector(`#div_edit${post_id}`).style.display = "block";
        document.querySelector(`#buttons${post_id}`).innerHTML = "";
    })
}

// from https://docs.djangoproject.com/en/3.0/ref/csrf/#ajax
function getCookie(name) {
    if (!document.cookie) {
      return null;
    }
    
    const token = document.cookie.split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith(name + '='));
  
    if (token.length === 0) {
      return null;
    }
    
    return decodeURIComponent(token[0].split('=')[1]);
 }