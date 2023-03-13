// funtion to handle the delete task request
function deleteNote(taskId){
    fetch('/delete-task',{
        method: 'POST',
        body: JSON.stringify({taskId:taskId})
    }).then((_res)=>{
        window.location.href="/";
    });
}
