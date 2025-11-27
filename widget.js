(function() {
  const widget = {
    init: function(config = {}) {
      const button = document.createElement('div');
      button.id = 'ccai-a2p-widget-button';
      button.innerHTML = '💬 A2P Compliance';
      button.style.cssText = 'position:fixed;bottom:20px;right:20px;background:#0066cc;color:white;padding:15px 20px;border-radius:50px;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.15);font-family:sans-serif;font-size:14px;z-index:9998;';
      
      const iframe = document.createElement('iframe');
      iframe.id = 'ccai-a2p-widget-iframe';
      iframe.src = 'https://main.d28k46xdno1z6x.amplifyapp.com';
      iframe.style.cssText = 'position:fixed;bottom:90px;right:20px;width:400px;height:600px;border:none;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,0.2);z-index:9999;display:none;';
      
      button.onclick = function() {
        iframe.style.display = iframe.style.display === 'none' ? 'block' : 'none';
      };
      
      document.body.appendChild(button);
      document.body.appendChild(iframe);
    }
  };
  
  window.CCAIA2PWidget = widget;
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      if (window.CCAIA2PWidget.autoInit !== false) {
        widget.init();
      }
    });
  } else {
    if (window.CCAIA2PWidget.autoInit !== false) {
      widget.init();
    }
  }
})();
