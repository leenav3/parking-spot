function deleteNote(noteId){
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId})
    }).then((_res) =>{
        window.location.href = "/";
    });
}


function updateSpot(spotId){
    fetch('/update-spot', {
        method: 'POST',
        body: JSON.stringify({spotId: spotId})
    }).then((_res) =>{
        alert("a")
        window.location.href = "/";
    });
}