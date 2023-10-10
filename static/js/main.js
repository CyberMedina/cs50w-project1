// Hazta que la página haya sido cargada, la animación de carga desaparece
document.addEventListener("DOMContentLoaded", function () {
    window.addEventListener('load', function () {
      var loader = document.querySelector(".loader");
      var preloader = document.getElementById("preloder");

      loader.style.opacity = "0";
      preloader.style.transition = "opacity 0.2s ease";
      preloader.style.opacity = "0";

      preloader.addEventListener('transitionend', function () {
        loader.style.display = "none";
        preloader.style.display = "none";
      });
    });

    

    // Aca indicamos que si en el localStorage existe la variable este deberá ejecutar el toast de "ha iniciado sesión correctamente"
    if (localStorage.getItem('inicioSesionPrimera')) {
      var toast = new bootstrap.Toast(document.getElementById('toastStatus'))
      // Selecciono el id de los componentes de mi toastStatus
      var titleToast = document.getElementById('titleToast');
      var bodyToast = document.getElementById('bodyToast');

      // Insertamos el texto a los componentes de mi toast
      titleToast.innerText = "Inicio de sesión con éxito"
      bodyToast.innerText = "Bienvenido a Lectoria!"

      var url = window.location.toString();
      if (url.indexOf("?registerSuccess=1") || url.indexOf("?reviewSucess=1") > 0) {
        var clean_url = url.substring(0, url.indexOf("?"));
        window.history.replaceState({}, document.title, clean_url);
      }


      toast.show();

      localStorage.removeItem('inicioSesionPrimera') // Ya que se imprimió debemos de eliminarlo, para que no siga apareciendo cada vez que se recargue la pantalla
    }



    // Hagarramos el botón de iniciar sesión de mi modal login #login-button y esperamos que haga click para correr el código
    document.querySelector("#login-button").addEventListener("click", function (e) {

      // Se chequea si los inputs del login son validos o no, mediante el uso de checkValidity

      var formLogin = document.getElementById('form-login');

      if (!formLogin.checkValidity()) {
        formLogin.reportValidity();
        return
      }


      // Se quita la función POST del botón para evitar que recargue la página
      e.preventDefault();

      var btn = document.querySelector("#login-button");
      btn.classList.add('disabled-button');



      // Se almacena toda la infromación del form del modal
      const formData = new FormData(document.querySelector(".form"));

      // Consulta al servidor para el correo y contraseña son validos
      fetch('/login_user', {
        method: 'POST',
        body: formData
      }).then(response => response.json()).then(data => {
        if (data.login_successful == 1) {
          console.log("Debería recargar")
          localStorage.setItem('inicioSesionPrimera', 'true')
          window.location.reload(); // Recargamos la página para que haga efecto la función session de nuestro backend
        }
        else {

          // Selecciono el id de los componentes de mi toastStatus
          var titleToast = document.getElementById('titleToast');
          var bodyToast = document.getElementById('bodyToast');

          //Selecciono el id del toast y el id para todo el formulario del login
          var toast = new bootstrap.Toast(document.getElementById('toastStatus'));
          var formLogin = document.getElementById('form-login');
          formLogin.reset(); // Elimino los campos de mi login

          // Insertamos el texto a los componentes de mi toast
          titleToast.innerText = "Error de inicio de sesión"
          bodyToast.innerText = "Mira chele, tus credenciales son incorrectas"

          // Devolvemos a habilitar el botón
          var loginButton = document.querySelector("#login-button");
          loginButton.classList.remove('disabled-button');

          // Cerramos el modal y abrimos el toast  con la información del inicio de sesión
          LoginModal.hide();
          toast.show();
        }
      });
    });

    // Esperamos que haga clic en el botón "buscar_libros" para ejecutar la consulta
    document.querySelector("#buscar_libros").addEventListener("click", function (e) {


      // Devolvemos a habilitar el botón
      var loginButton = document.querySelector("#login-button");
      loginButton.classList.remove('disabled-button');

      var buscar_libros = document.querySelector('#buscar_libros')
      buscar_libros.classList.add('disabled-button')

      e.preventDefault(); // Detiene la redirección
      console.log("click");

      // Llamada AJAX para comprobar si se necesita autenticación
      fetch('/check_logged').then(response => response.json()).then(data => {
        if (data.logged_in == 2) {

          // Selecciono el id de los componentes de mi toastStatus
          var titleToast = document.getElementById('titleToast');
          var bodyToast = document.getElementById('bodyToast');

          //Selecciono el id del toast y el id para todo el formulario del login
          var toast = new bootstrap.Toast(document.getElementById('toastStatus'));
          var formLogin = document.getElementById('form-login');
          formLogin.reset(); // Elimino los campos de mi login

          // Insertamos el texto a los componentes de mi toast
          titleToast.innerText = "Error"
          bodyToast.innerText = "Debes de iniciar sesión primero!"
          buscar_libros.classList.remove('disabled-button') // Cuando llegue la respuesta al servidor habilitamos de nuevo el botón


          abrirLogin('loginModal');
          toast.show();

        }

        if (data.logged_in == 1) {
          console.log("Redirigiendo a search")
          // Si no necesita iniciar sesión, redirige como normalmente
          window.location.href = "/search";
          buscar_libros.classList.remove('disabled-button') // Cuando llegue respuesta del servidor volvemos a habilitar el botón
        }
      });
    });
  });
