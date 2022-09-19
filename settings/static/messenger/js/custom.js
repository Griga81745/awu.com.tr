/*
    - back button in chat navar (on mobile)
    - user section in users list 
*/
const mobileToggleChat = () =>{
    document.querySelector('.user-chat').classList.toggle('user-chat-show')
}


/*
    - close button in profile sidebar
    - back button in profile sidebar
    - user fullname in chat navbar
*/
const toggleProfileSidebar = () => {
    document.querySelector('#userProfileSidebar').classList.toggle('d-block')
}