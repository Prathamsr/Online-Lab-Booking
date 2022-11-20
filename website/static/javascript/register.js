const pre=document.querySelector(".previewimage");
const given_img=document.querySelector("#profile_pic");
const img =document.querySelector("#hello");
given_img.addEventListener("change", function(){
    const file=this.files[0];
    const reader= new FileReader();
    reader.onload=function(){
        const result=reader.result;
        img.src=result;
    };
    reader.readAsDataURL(file);
});
