document.addEventListener("DOMContentLoaded", () => {
    
    const peerID = JSON.parse(document.getElementById('peer-id')?.textContent);
    const peerAvatarURL = JSON.parse(document.getElementById('peer-avatar-url')?.textContent);
    const currentID = JSON.parse(document.getElementById('current-id').textContent);

    const messageContainer = document.querySelector('#chat-conversation > div.simplebar-wrapper > div.simplebar-mask > div > div')
    messageContainer.scroll(0,messageContainer.scrollHeight)

    const messageTemplatePeer = (text,datetime) => {
        return /*html*/ `
            <li class="chat-list left" id="3">                        
                <div class="conversation-list">
                    <div class="chat-avatar">
                        <img src="${peerAvatarURL}" alt="" style="object-fit:cover">
                    </div>
                    <div class="user-chat-content">
                        <div class="ctext-wrap">
                            <div class="ctext-wrap-content" id="3">        
                                <p class="mb-0 ctext-content">${text}</p>
                            </div>
                            <div class="dropdown align-self-start message-box-drop">                
                                <a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">                    
                                    <i class="ri-more-2-fill"></i>                
                                </a>                
                                <div class="dropdown-menu">                                       
                                    <a 
                                        class="dropdown-item d-flex align-items-center justify-content-between copy-message" 
                                        href="#" id="copy-message-0">
                                        Copy <i class="bx bx-copy text-muted ms-2"></i>
                                    </a>                    
                                </div>            
                            </div>
                        </div>
                        <div class="conversation-name">
                            <small class="text-muted time">${datetime}</small> 
                            <span class="text-success check-message-icon">
                                <i class="bx bx-check-double"></i>
                            </span>
                        </div>
                    </div>                
                </div>            
            </li>
        `
    }

    const messageTemplate = (text,datetime) => {
        return /*html*/`
            <li class="chat-list right" id="5">                        
                <div class="conversation-list">
                    <div class="user-chat-content">
                        <div class="ctext-wrap">
                            <div class="ctext-wrap-content" id="5">        
                                <p class="mb-0 ctext-content">${text}</p>
                            </div>
                            <div class="dropdown align-self-start message-box-drop">                
                                <a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    <i class="ri-more-2-fill"></i>                
                                </a>                 
                                <div class="dropdown-menu">                    
                                    <a class="dropdown-item d-flex align-items-center justify-content-between copy-message" href="#" id="copy-message-0">
                                        Copy <i class="bx bx-copy text-muted ms-2"></i>
                                    </a>               
                                </div>            
                            </div>
                        </div>
                        <div class="conversation-name">
                            <small class="text-muted time">${datetime}</small> 
                            <span class="text-success check-message-icon">
                                <i class="bx bx-check-double"></i>
                            </span>
                        </div>
                    </div>                
                </div>            
            </li>
        `
    }

    const chatSocket = new WebSocket(
        `${location.protocol==='https'?'wss':'ws'}://`
        + window.location.host
        + '/ws/chat/'
        + peerID
        + '/'
    );

    chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);

        switch (data.type)
        {
            case 'new_message': 
            {
                if (peerID === data.peer_id)
                {
                    // if there is active chat
                    document.querySelector('#users-conversation').insertAdjacentHTML(
                        'beforeend',
                        data.peer_id === currentID ? messageTemplate(data.message,data.sent_datetime) : messageTemplatePeer(data.message,data.sent_datetime));
                    messageContainer.scroll(0,messageContainer.scrollHeight);
                }
                else if (peerID !== data.peer_id)
                {
                    // to update sidebar during new messages
                    let unreadenBadge = document.querySelector(`#messengerChat${data.sender_id} .badge`)
                    unreadenBadge.innerHTML++ 
                }
                break
            }

            case 'peer_online': 
            {
                let online_text = 'Cevrimiçi' 
                let offline_text = 'Cevrimdışı'

                let currentPeerOnlineTextClass = 'peerOnline'
                let currentPeerOnlineDotClass = 'peerOnlineDot'

                let sidebarPeerIDPrefix = 'messengerChat'
                let sidebarPeerOnlineDotClass = 'user-status'

                if (peerID === data.peer_id)
                {
                    document.getElementsByClassName(currentPeerOnlineTextClass)
                        .forEach(element => element.innerHTML = data.status ? online_text : offline_text)
                    document.querySelectorAll(currentPeerOnlineDotClass)
                        .forEach(element => element.style.opacity = data.status? '1' : '0' )
                }
                else if (peerID !== data.peer_id)
                {
                    document
                        .querySelector(`#${sidebarPeerIDPrefix}${data.peer_id} .${sidebarPeerOnlineDotClass}`)
                        .style.opacity = data.status? '1' : '0'

                }
                break
            } 
        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) 
        {
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message,
        }));
        messageInputDom.value = '';
    };
});
