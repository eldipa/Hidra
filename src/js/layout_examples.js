define(['jquery', 'layout'], function ($, layout) {
   function init() {
      var Root = layout.Root;
      var Panel = layout.Panel;

      /*
       * El sistema de layout esta compuesto por una serie de objetos 'Panel' que
       * se encargan de dibujar su contenido en la pantalla.
       *
       * Para comenzar, crearemos un panel que muestra un simple mensaje.
       * */
      
      var hello_msg = new Panel();
 
      hello_msg.msg = 'hello world';     
      hello_msg.render = function () {
         $(this.box).html(this.msg);
      };

      /* 
       * Como se puede ver, el unico requerimiento es que el panel defina un
       * metodo llamado 'render' para que renderize en el DOM.
       * 
       * La property 'box' contiene un objeto que representa un objeto DIV
       * en el DOM donde se puede renderizar.
       *
       * Aun asi, nuestro panel no se dibuja en la pantalla hasta que sea
       * insertado en el DOM de la aplicacion.
       *
       * Para esto crearemos un objeto Root que se attachara al 'body' del DOM.
       * */

      var root = new Root($('body'));

      /* Ahora solo nos falta insertar nuestro panel en el root. */

      root.push(hello_msg);

      /* --------- XXX ------------- */

      /* Listo.
       *
       * Si queremos, podemos cambiar la funcion render para cambiar el mensaje
       * (podriamos cambiar una property u otra cosa para cambiar el mensaje, 
       * no es necesario cambiar todo el render).
       *
       * Para que el cambio surja efecto, debemos refrescar el panel.
       *
       * */

      hello_msg.msg = hello_msg.msg + '<br />hello world!!!';
      hello_msg.refresh();

      /* --------- XXX ------------- */

      /* Con solo un panel, no hay mucha diferencia entre esto y simplemente
       * renderizar en el DOM.
       *
       * Todo panel puede dividirse en 2, ya sea horizontal o verticalmente
       * agregando otro panel mas a la escena.
       * */

      var bye_bye_msg = new Panel();
      bye_bye_msg.msg = 'Bye Bye Bye';
      bye_bye_msg.render = function () {
         $(this.box).html(this.msg);
      };

      hello_msg.split(bye_bye_msg, 'left');
      root.refresh();

   }

   return {init: init};
});