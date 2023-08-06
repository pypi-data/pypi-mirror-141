 .. raw:: html

  <br><br><br><br><br>

 **{{ fullname }}**

 .. automodule:: {{ fullname }}

     {% block exceptions %}
     {% if exceptions %}
     .. rubric:: exceptions

     .. autosummary::
     {% for item in exceptions %}
         {{ item }}
     {%- endfor %}
     {% endif %}
     {% endblock %}

     {% block classes %}
     {% if classes %}
     .. rubric:: classes

     .. autosummary::
     {% for item in classes %}
         {{ item }}
     {%- endfor %}
     {% endif %}
     {% endblock %}

     {% block functions %}
     {% if functions %}
     .. rubric:: functions

     .. autosummary::
     {% for item in functions %}
         {{ item }}
     {%- endfor %}
     {% endif %}
     {% endblock %}

 .. title:: {{ fullname }}

