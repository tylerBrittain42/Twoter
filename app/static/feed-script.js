console.log("feed-script called");

// Tweet limit counter
var textCount = document.getElementById("content");
var result = document.getElementById("result");
var limit = 145;
result.textContent = 0 + "/" + limit;
textCount.addEventListener("input", function () {
  var length = textCount.value.length;
  result.textContent = length + "/" + limit;
});

function deleteTwote(this_ele) {
  if(confirm("Are you sure you want to delete this twowte?")){
  console.log("delete clicked");
  const ele = {
    name: document.getElementById("twotecontent").id,
  };
  twote_id = this_ele.id;
  fetch(`http://127.0.0.1:5000/twote?twote_id=${twote_id}`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(ele),
  })
    .then((response) => response.json())
    .then((data) => console.log(data))
    .then(() => location.reload());
}
}

function cannotOpen(){
  alert('ERROR: Cannot Edit')
  return
}

function cannotDelete(){
  alert('ERROR: Cannot Delete')
  return
}

//Opens window when 'edit' button is pressed
function openForm(this_ele) {
  console.log(this_ele)
  document.getElementById("myForm").style.display = "block";
  const to_remove = document.querySelector(".active");
  console.log(to_remove);
  if (to_remove != null) {
    to_remove.classList.remove("active");
  }
  this_ele.classList.add("active");
}
//Closes window
function closeForm() {
  document.getElementById("myForm").style.display = "none";
}
//word count

function updateTwote(this_ele) {
  event.preventDefault();
  console.log("update called");
  const updated_body = document.querySelector("#editcontent").value;

  const ele = {
    editcontent: updated_body,
    twote_id: document.querySelector(".active").id,
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
    .then(() => location.reload());
}
