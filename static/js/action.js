const content1 = document.getElementById("content1");
const content2 = document.getElementById("content2");
const loading = document.getElementById("loading");

window.addEventListener('load',()=> {
    loading.style.display = "none";
    content1.style.display = "initial";
    content2.style.display = "initial";
})

function loading_animation(){
    loading.style.display = "flex";
    content1.style.display = "none";
    content2.style.display = "none";
}

function goBack(){
    window.location.href=document.referrer;
}

function info(){
    window.alert('The Opration was Successful');
    goBack();
}

// notifcation
function notifcation(subject,stute){
    var note = document.getElementById('note');
    var title = document.getElementById('title');
    console.log(title);
    var subject = document.getElementById('subject');
    if (stute == 'error'){
        note.style.display = 'block';
        title.innerHTML = stute;
        subject.innerHTML = subject;//'Task completed successfully!!'
    } else {
        note.style.display = 'block';
        title.innerHTML = stute;
        note.innerHTML = subject;
    }
    setTimeout(function(){
        note.style.display = 'none';
    }, 1500);
}

function dropdown(){
    const dropdown = document.getElementById('drop');
    dropdown.classList.toggle('show');
  }
  window.addEventListener('click',function(event){
    if(!event.target.matches('.btn')){
      const dropdown = document.getElementById('drop');
      if(dropdown.classList.contains('show')){
        dropdown.classList.remove('show');
      }
    }
  });
