(function disqus_comments(){
var disqusPublicKey = "ovehkBUyCGwYkxkfEX9ZG5LRLk5dC4VO0M4zKyVSXMEW9DNIOmSQb2rRpfJ4v3y8";
var disqusShortname = "zaresdelaweb";
var urlArray = [];
$('.post-comments').each(function () {
  var url = $(this).attr('data-disqus-url');
  urlArray.push('link:' + url);
});
$.ajax({
  type: 'GET',
  url: "https://disqus.com/api/3.0/threads/set.jsonp",
  data: { api_key: disqusPublicKey, forum : disqusShortname, thread : urlArray },
  cache: false,
  dataType: 'jsonp',
  success: function (result) {
    for (var i in result.response) {
      var countText = " comments";
      var count = result.response[i].posts;

      if (count == 1){
        countText = " comment";
      }
      $('a[data-disqus-url="' + result.response[i].link + '"]').html(count + countText);

    }
  }
});
})();
