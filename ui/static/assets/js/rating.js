function lidi (inst) {
    //  hWrap : html like/dislike container
    //  change : function to handle like/dislike toggle change
    //  status : -1 dislike, 0 neutral, 1 like (optional, default 0)
    //  count : [likes, dislikes] (optional)
    
      // (A) DEFAULT STATUS + CSS WRAPPER CLASS
      if (!inst.status) { inst.status = 0; }
      inst.hWrap.classList.add("lidiWrap");
    
      // (B) ATTACH LIKE & DISLIKE BUTTON
      inst.hUp = document.createElement("div");
      inst.hDown = document.createElement("div");
      inst.hUp.className = "lidiUp";
      inst.hDown.className = "lidiDown";
      if (inst.status==1) { inst.hUp.classList.add("set"); }
      if (inst.status==-1) { inst.hDown.classList.add("set"); }
      inst.hWrap.appendChild(inst.hUp);
      inst.hWrap.appendChild(inst.hDown);
    
      // (D) TOGGLE LIKE/DISLIKE
      inst.updown = up => {
        // (D1) UPDATE STATUS FLAG
        if (up) { inst.status = inst.status == 1 ? 0 : 1; }
        else { inst.status = inst.status == -1 ? 0 : -1; }
    
        // (D2) UPDATE LIKE/DISLIKE CSS
        if (inst.status==1) {
          inst.hUp.classList.add("set");
          inst.hDown.classList.remove("set");
        } else if (inst.status==-1) {
          inst.hUp.classList.remove("set");
          inst.hDown.classList.add("set");
        } else {
          inst.hUp.classList.remove("set");
          inst.hDown.classList.remove("set");
        }
    
        // (D3) TRIGGER CHANGE
        inst.change(inst.status);
      };
      inst.hUp.onclick = () => { inst.updown(true); };
      inst.hDown.onclick = () => { inst.updown(false); };
    
      // (E) ENABLE/DISABLE
      inst.enable = () => {
        inst.hUp.onclick = () => { inst.updown(true); };
        inst.hDown.onclick = () => { inst.updown(false); };
      };
      inst.disable = () => {
        inst.hUp.onclick = "";
        inst.hDown.onclick = "";
      };
      inst.enable();
      
      // (F) DONE
      return inst;
    }
    
    // (G) ATTACH LIKE DISLIKE BUTTON
    window.onload = () => {
      let name = getCookie('filename')
      let event = 'rating-event'
      eraseCookie('filename')
      var lidiA = lidi({
        hWrap : document.getElementById("lidiA"),
        change : status => { 
          console.log(status); 
          setCookie(event, 'filename='+ name + '&value='+status)
        }
      });
    
    };


  /*--------------------------------------------------------------
    19. Interacting with Cookies
  --------------------------------------------------------------*/
  function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
  }
  function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
  }
  function eraseCookie(name) {   
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  }
    