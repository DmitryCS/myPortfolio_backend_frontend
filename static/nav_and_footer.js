document.getElementById("insertNavMenu").innerHTML = 
        `<nav class="menu">
            <ul>        
                <li><a href="/"><i class="fa fa-home fa-fw"></i>Who am I?</a></li>        
                <li><a href="skills.html">Do I have skills?</a></li>        
                <li><a href="langs.html">Do I know computer languages?</a></li>        
                <li><a href="ican.html">What can I do?</a></li>           
                <li><a href="exs.html">Examples of work</a></li>
                <li><a href="grid.html">Grid of people</a></li>
                <li id="lgn" class="before_last"><a href="login.html">Login</a></li>
                <li id="lgn2"><a href="register.html">Register</a></li>               
            </ul>
<!--             <ul class="secondUL">-->
<!--                <li id="lgn" class="before_last"><a href="login.html">Login</a></li>-->
<!--                <li id="lgn2"><a href="register.html">Register</a></li>             -->
<!--            </ul>-->
        </nav>`;
        if(document.cookie!=""){
                document.getElementById("lgn").innerHTML = `<a href="profile.html">${document.cookie}</a>`;
                document.getElementById("lgn2").innerHTML = `<a href="logout.html">Logout</a>`;
        }
        document.getElementById("insertFooter").innerHTML = `
        <div class="footer">
            <h1>Links to me</h1>          
            <ul>                
                <li><a href="https://vk.com/dimacs"><img src="../static/images/vk.svg" height="100" width="100"></a></li>
                <li><a href="https://github.com/DmitryCS"><img src="../static/images/github.svg" height="100" width="100"></a></li>
                <!--<li><a href="https://app.codesignal.com/profile/dmitrycs"><img src="../static/images/codesignal.jpg" height="100" width="100"></a></li>-->
                <li><a href="https://codeforces.com/profile/Phantom_"><img src="../static/images/cdf.png" height="100" width="100"></a></li>
                <li><a href="https://stepik.org/users/82724021"><img src="../static/images/stepik.svg" height="100" width="100"></a></li>                                
            </ul>
        </div>`;