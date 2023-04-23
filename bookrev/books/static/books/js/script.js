var replyBtns = document.querySelectorAll('.reply-btn');
  replyBtns.forEach(function(replyBtn) {
    replyBtn.addEventListener('click', function() {
      var commentId = this.getAttribute('data-id');
      var replyForm = document.querySelector('#reply-form-' + commentId);
      replyForm.style.display = replyForm.style.display === 'none' ? 'block' : 'none';
    });
  });