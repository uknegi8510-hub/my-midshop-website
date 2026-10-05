let rating=4.5;
    let totalstars=5;
    let html="";

    for (i=1;i<totalstars;i++){
        if(i <= rating){
            html+='<i class="fa-solid fa-star"style="color:#08a94b;"></i>';
        }else if(i-rating===0.5){
             html += '<i class="fa-solid fa-star-half-stroke"style="color:#08a94b;"></i>';
        }else{
             html += '<i class="fa-regular fa-star"style="color:#08a94b;"></i>';

        }
    }   
    html += '<span class="review-count">(121)</span>';
    document.getElementById('rating').innerHTML = html;

    let count=0;
    function increase(){
        count++;
        document.getElementById("qty").innerText=count;
    }
    function decrease(){
        if (count >1){
            count--;
            document.getElementById("qty").innerText=count;
        }
        else{
            document.getElementById("qty").innerText=0;
        }

    }

// heart section
document.querySelectorAll('.heart').forEach(heart => {
    heart.addEventListener('click', function () {
      this.classList.toggle('active');
    });
  });


const container = document.getElementById("imagescroll");

function updateProgress() {
  console.log(
    "Scroll Left:", container.scrollLeft,
    "Max Scroll:", container.scrollWidth - container.clientWidth
  );
}

container.addEventListener("scroll", updateProgress);
window.addEventListener("load", updateProgress);

