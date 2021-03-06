tweetLimitCounter();


function tweetLimitCounter(){
  // Tweet limit counter
  var textCount = document.getElementById("content");
  var result = document.getElementById("result");
  var limit = 145;
  result.textContent = 0 + "/" + limit;
  textCount.addEventListener("input", function () {
    var length = textCount.value.length;
    result.textContent = length + "/" + limit;
  });
}


function deleteTwote(this_ele) {
  if(confirm("Are you sure you want to delete this twote?")){
    console.log("delete clicked");
    const ele = {
      name: document.getElementById("twotecontent").id,
    };
    twote_id = this_ele.id;
    fetch(`http://127.0.0.1:5000/twote?twote_id=${twote_id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json",
                  "Accept": "application/json"},
      body: JSON.stringify(ele),
    })
      //.then((response) => response.json())
      //.then((data) => console.log(data))
      .then(() =>{window.location.reload()});
  }
}

function cannotOpen(){
  alert('ERROR: Cannot Edit')
  return
}



//Opens window when 'edit' button is pressed
function openForm(this_ele) {
  console.log(this_ele)
  document.getElementById("myForm").style.display = "block";
  // const to_remove = document.querySelector(".active");
  const to_remove = document.querySelector('.active-edit')
  console.log(to_remove);
  if (to_remove != null) {
    to_remove.classList.remove("active");
    to_remove.classList.remove("active-edit")
  }
  this_ele.classList.add("active");
  this_ele.classList.add('active-edit');
}
//Closes window
function closeForm() {
  document.getElementById("myForm").style.display = "none";
}

function cannotDelete(){
  alert('ERROR: Cannot Delete')
  return
}

function updateTwote(this_ele) {
  event.preventDefault();
  console.log("update called");
  const updated_body = document.querySelector("#editcontent").value;

  const ele = {
    editcontent: updated_body,
    twote_id: document.querySelector(".active-edit").id,
  };
  //console.log(document.querySelector('.active').id  )
  //return
  //const content = form.elements.action.value;
  //const twote_id = form.elements.action.value;

  fetch(`http://127.0.0.1:5000/twote`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(ele),
  })
    .then((res) => res)
    .then((data) => console.log(data))
    .then(() => {
      window.location.reload();
    });
}

function likeTwote(this_ele) {
  console.log("like clicked");
  const ele = {
    name: document.getElementById("content").id,
  };
  twote_id = this_ele.id;
  fetch(`http://127.0.0.1:5000/like/${twote_id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(ele),
  })
    .then((response) => response)
    .then((data) => console.log(data))
    .then(() => window.location.reload());
}

function unlikeTwote(this_ele) {
  console.log("unlike clicked");
  const ele = {
    name: document.getElementById("content").id,
  };
  twote_id = this_ele.id;
  fetch(`http://127.0.0.1:5000/unlike/${twote_id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(ele),
  })
    .then((response) => response)
    .then((data) => console.log(data))
    .then(() => window.location.reload());
}


function likeHandler(ele){
  if (ele.classList.contains('is-liked'))
    unlikeTwote(ele)
  else
    likeTwote(ele)
}

function retwoteHandler(ele){
  if (ele.classList.contains('is-retwot'))
    unreTwote(ele.id)
  else
    reTwote(ele.id)
}

function reTwote(twote_id){

  fetch(`http://127.0.0.1:5000/retwote/${twote_id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" }
    // body: JSON.stringify(ele),
  })
    .then(() => window.location.reload());

}

function unreTwote(twote_id){
  console.log('unretwote clicked')
  fetch(`http://127.0.0.1:5000/unretwote/${twote_id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" }
    // body: JSON.stringify(ele),
  })
    .then(() => window.location.reload());

}

function noFollow(){
  alert('Cannot follow self')
}