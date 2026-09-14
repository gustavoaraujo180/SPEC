import zipfile
import json
import os

# Define project configuration
APP_PACKAGE = "appinventor.ai_student.MultiCalcApp"
PROJECT_PROPERTIES = """main=appinventor.ai_student.MultiCalcApp.Screen1
name=MultiCalcApp
assets=../assets
source=../src
build=../build
versioncode=1
versionname=1.0
useslocation=false
aname=MultiCalcApp
"""

# Helper to create .scm file content
def make_scm(form_name, title, components):
    scm_dict = {
        "authURL": [],
        "YaVersion": "208",
        "Source": "Form",
        "Properties": {
            "$Name": form_name,
            "$Type": "Form",
            "$Components": components,
            "AppName": "MultiCalcApp",
            "Title": title,
            "AlignHorizontal": "3",  # Center
            "AlignVertical": "1",    # Top
            "BackgroundColor": "&HFFFFFFFF", # White background
            "PrimaryColor": "&HFF2196F3",
            "AccentColor": "&HFF009688"
        }
    }
    return "#$JSON\n" + json.dumps(scm_dict, indent=2)

# --- Screen 1: LOGIN ---
screen1_components = [
    {
        "$Name": "LabelTitulo",
        "$Type": "Label",
        "Text": "LOGIN",
        "FontSize": "24",
        "FontBold": "True",
        "TextAlignment": "1"
    },
    {
        "$Name": "LabelUsuario",
        "$Type": "Label",
        "Text": "Usuário",
        "FontSize": "16"
    },
    {
        "$Name": "TextBoxUsuario",
        "$Type": "TextBox",
        "Hint": "Digite seu usuário",
        "Width": "-2"
    },
    {
        "$Name": "LabelSenha",
        "$Type": "Label",
        "Text": "Senha",
        "FontSize": "16"
    },
    {
        "$Name": "TextBoxSenha",
        "$Type": "PasswordTextBox",
        "Hint": "Digite sua senha",
        "Width": "-2"
    },
    {
        "$Name": "ButtonEntrar",
        "$Type": "Button",
        "Text": "ENTRAR",
        "FontSize": "18",
        "Width": "-2"
    },
    {
        "$Name": "LabelMensagem",
        "$Type": "Label",
        "Text": "",
        "FontSize": "16",
        "TextColor": "&HFFFF0000"
    }
]

screen1_bky = """<xml xmlns="http://www.w3.org/1999/xhtml">
  <block type="component_event" id="b_login_click" x="30" y="30">
    <mutation component_type="Button" is_generic="false" instance_name="ButtonEntrar" event_name="Click"></mutation>
    <field name="COMPONENT_SELECTOR">ButtonEntrar</field>
    <statement name="DO">
      <block type="controls_if" id="b_if_login">
        <mutation else="1"></mutation>
        <value name="IF0">
          <block type="logic_operation" id="b_and">
            <field name="OP">AND</field>
            <value name="A">
              <block type="logic_compare" id="b_check_user">
                <field name="OP">EQ</field>
                <value name="A">
                  <block type="component_set_get" id="b_get_user">
                    <mutation component_type="TextBox" instance_name="TextBoxUsuario" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                    <field name="COMPONENT_SELECTOR">TextBoxUsuario</field>
                    <field name="PROP">Text</field>
                  </block>
                </value>
                <value name="B">
                  <block type="text" id="b_txt_admin">
                    <field name="TEXT">admin</field>
                  </block>
                </value>
              </block>
            </value>
            <value name="B">
              <block type="logic_compare" id="b_check_pass">
                <field name="OP">EQ</field>
                <value name="A">
                  <block type="component_set_get" id="b_get_pass">
                    <mutation component_type="PasswordTextBox" instance_name="TextBoxSenha" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                    <field name="COMPONENT_SELECTOR">TextBoxSenha</field>
                    <field name="PROP">Text</field>
                  </block>
                </value>
                <value name="B">
                  <block type="text" id="b_txt_pass">
                    <field name="TEXT">1234</field>
                  </block>
                </value>
              </block>
            </value>
          </block>
        </value>
        <statement name="DO0">
          <block type="controls_openAnotherScreen" id="b_open_screen2">
            <value name="SCREEN">
              <block type="text" id="b_scr2_title">
                <field name="TEXT">Screen2</field>
              </block>
            </value>
          </block>
        </statement>
        <statement name="ELSE">
          <block type="component_set_get" id="b_set_msg">
            <mutation component_type="Label" instance_name="LabelMensagem" property_name="Text" is_generic="false" get_or_set="set"></mutation>
            <field name="COMPONENT_SELECTOR">LabelMensagem</field>
            <field name="PROP">Text</field>
            <value name="VALUE">
              <block type="text" id="b_err_msg">
                <field name="TEXT">Usuário ou senha incorretos!</field>
              </block>
            </value>
          </block>
        </statement>
      </block>
    </statement>
  </block>
</xml>"""

# --- Screen 2: MENU PRINCIPAL ---
screen2_components = [
    {
        "$Name": "LabelTitulo",
        "$Type": "Label",
        "Text": "MENU PRINCIPAL",
        "FontSize": "24",
        "FontBold": "True",
        "TextAlignment": "1"
    },
    {
        "$Name": "ButtonCalculadora",
        "$Type": "Button",
        "Text": "CALCULADORA",
        "FontSize": "18",
        "Width": "-2"
    },
    {
        "$Name": "ButtonIMC",
        "$Type": "Button",
        "Text": "CALCULAR IMC",
        "FontSize": "18",
        "Width": "-2"
    },
    {
        "$Name": "ButtonMedia",
        "$Type": "Button",
        "Text": "MÉDIA ESCOLAR",
        "FontSize": "18",
        "Width": "-2"
    },
    {
        "$Name": "ButtonSair",
        "$Type": "Button",
        "Text": "SAIR",
        "FontSize": "18",
        "Width": "-2"
    }
]

screen2_bky = """<xml xmlns="http://www.w3.org/1999/xhtml">
  <block type="component_event" id="b_calc_click" x="30" y="30">
    <mutation component_type="Button" is_generic="false" instance_name="ButtonCalculadora" event_name="Click"></mutation>
    <field name="COMPONENT_SELECTOR">ButtonCalculadora</field>
    <statement name="DO">
      <block type="controls_openAnotherScreen" id="b_open_screen3">
        <value name="SCREEN">
          <block type="text" id="b_scr3_title">
            <field name="TEXT">Screen3</field>
          </block>
        </value>
      </block>
    </statement>
  </block>
  <block type="component_event" id="b_imc_click" x="30" y="130">
    <mutation component_type="Button" is_generic="false" instance_name="ButtonIMC" event_name="Click"></mutation>
    <field name="COMPONENT_SELECTOR">ButtonIMC</field>
    <statement name="DO">
      <block type="controls_openAnotherScreen" id="b_open_screen4">
        <value name="SCREEN">
          <block type="text" id="b_scr4_title">
            <field name="TEXT">Screen4</field>
          </block>
        </value>
      </block>
    </statement>
  </block>
  <block type="component_event" id="b_media_click" x="30" y="230">
    <mutation component_type="Button" is_generic="false" instance_name="ButtonMedia" event_name="Click"></mutation>
    <field name="COMPONENT_SELECTOR">ButtonMedia</field>
    <statement name="DO">
      <block type="controls_openAnotherScreen" id="b_open_screen5">
        <value name="SCREEN">
          <block type="text" id="b_scr5_title">
            <field name="TEXT">Screen5</field>
          </block>
        </value>
      </block>
    </statement>
  </block>
  <block type="component_event" id="b_sair_click" x="30" y="330">
    <mutation component_type="Button" is_generic="false" instance_name="ButtonSair" event_name="Click"></mutation>
    <field name="COMPONENT_SELECTOR">ButtonSair</field>
    <statement name="DO">
      <block type="controls_closeApplication" id="b_close_app"></block>
    </statement>
  </block>
</xml>"""

# --- Screen 3: CALCULADORA ---
screen3_components = [
    {
        "$Name": "LabelTitulo",
        "$Type": "Label",
        "Text": "CALCULADORA",
        "FontSize": "24",
        "FontBold": "True",
        "TextAlignment": "1"
    },
    {
        "$Name": "TextBoxNumero1",
        "$Type": "TextBox",
        "Hint": "Primeiro número",
        "NumbersOnly": "True",
        "Width": "-2"
    },
    {
        "$Name": "TextBoxNumero2",
        "$Type": "TextBox",
        "Hint": "Segundo número",
        "NumbersOnly": "True",
        "Width": "-2"
    },
    {
        "$Name": "HorizontalArrangement1",
        "$Type": "HorizontalArrangement",
        "Width": "-2",
        "AlignHorizontal": "3",
        "$Components": [
            {
                "$Name": "ButtonSoma",
                "$Type": "Button",
                "Text": "+",
                "FontSize": "20",
                "Width": "-1"
            },
            {
                "$Name": "ButtonSubtracao",
                "$Type": "Button",
                "Text": "-",
                "FontSize": "20",
                "Width": "-1"
            },
            {
                "$Name": "ButtonMultiplicacao",
                "$Type": "Button",
                "Text": "×",
                "FontSize": "20",
                "Width": "-1"
            },
            {
                "$Name": "ButtonDivisao",
                "$Type": "Button",
                "Text": "÷",
                "FontSize": "20",
                "Width": "-1"
            }
        ]
    },
    {
        "$Name": "LabelResultado",
        "$Type": "Label",
        "Text": "Resultado:",
        "FontSize": "18",
        "FontBold": "True"
    },
    {
        "$Name": "ButtonVoltar",
        "$Type": "Button",
        "Text": "VOLTAR",
        "FontSize": "18",
        "Width": "-2"
    }
]

screen3_bky = """<xml xmlns="http://www.w3.org/1999/xhtml">
  <block type="component_event" id="b_soma_click" x="30" y="30">
    <mutation component_type="Button" is_generic="false" instance_name="ButtonSoma" event_name="Click"></mutation>
    <field name="COMPONENT_SELECTOR">ButtonSoma</field>
    <statement name="DO">
      <block type="component_set_get" id="b_set_res_soma">
        <mutation component_type="Label" instance_name="LabelResultado" property_name="Text" is_generic="false" get_or_set="set"></mutation>
        <field name="COMPONENT_SELECTOR">LabelResultado</field>
        <field name="PROP">Text</field>
        <value name="VALUE">
          <block type="text_join" id="b_join_soma">
            <mutation items="2"></mutation>
            <value name="ADD0">
              <block type="text" id="b_prefix_soma">
                <field name="TEXT">Resultado: </field>
              </block>
            </value>
            <value name="ADD1">
              <block type="math_add" id="b_add">
                <value name="NUM0">
                  <block type="component_set_get" id="b_get_n1_soma">
                    <mutation component_type="TextBox" instance_name="TextBoxNumero1" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                    <field name="COMPONENT_SELECTOR">TextBoxNumero1</field>
                    <field name="PROP">Text</field>
                  </block>
                </value>
                <value name="NUM1">
                  <block type="component_set_get" id="b_get_n2_soma">
                    <mutation component_type="TextBox" instance_name="TextBoxNumero2" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                    <field name="COMPONENT_SELECTOR">TextBoxNumero2</field>
                    <field name="PROP">Text</field>
                  </block>
                </value>
              </block>
            </value>
          </block>
        </value>
      </block>
    </statement>
  </block>

  <block type="component_event" id="b_sub_click" x="30" y="200">
    <mutation component_type="Button" is_generic="false" instance_name="ButtonSubtracao" event_name="Click"></mutation>
    <field name="COMPONENT_SELECTOR">ButtonSubtracao</field>
    <statement name="DO">
      <block type="component_set_get" id="b_set_res_sub">
        <mutation component_type="Label" instance_name="LabelResultado" property_name="Text" is_generic="false" get_or_set="set"></mutation>
        <field name="COMPONENT_SELECTOR">LabelResultado</field>
        <field name="PROP">Text</field>
        <value name="VALUE">
          <block type="text_join" id="b_join_sub">
            <mutation items="2"></mutation>
            <value name="ADD0">
              <block type="text" id="b_prefix_sub">
                <field name="TEXT">Resultado: </field>
              </block>
            </value>
            <value name="ADD1">
              <block type="math_subtract" id="b_sub">
                <value name="A">
                  <block type="component_set_get" id="b_get_n1_sub">
                    <mutation component_type="TextBox" instance_name="TextBoxNumero1" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                    <field name="COMPONENT_SELECTOR">TextBoxNumero1</field>
                    <field name="PROP">Text</field>
                  </block>
                </value>
                <value name="B">
                  <block type="component_set_get" id="b_get_n2_sub">
                    <mutation component_type="TextBox" instance_name="TextBoxNumero2" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                    <field name="COMPONENT_SELECTOR">TextBoxNumero2</field>
                    <field name="PROP">Text</field>
                  </block>
                </value>
              </block>
            </value>
          </block>
        </value>
      </block>
    </statement>
  </block>

  <block type="component_event" id="b_mul_click" x="30" y="370">
    <mutation component_type="Button" is_generic="false" instance_name="ButtonMultiplicacao" event_name="Click"></mutation>
    <field name="COMPONENT_SELECTOR">ButtonMultiplicacao</field>
    <statement name="DO">
      <block type="component_set_get" id="b_set_res_mul">
        <mutation component_type="Label" instance_name="LabelResultado" property_name="Text" is_generic="false" get_or_set="set"></mutation>
        <field name="COMPONENT_SELECTOR">LabelResultado</field>
        <field name="PROP">Text</field>
        <value name="VALUE">
          <block type="text_join" id="b_join_mul">
            <mutation items="2"></mutation>
            <value name="ADD0">
              <block type="text" id="b_prefix_mul">
                <field name="TEXT">Resultado: </field>
              </block>
            </value>
            <value name="ADD1">
              <block type="math_multiply" id="b_mul">
                <value name="NUM0">
                  <block type="component_set_get" id="b_get_n1_mul">
                    <mutation component_type="TextBox" instance_name="TextBoxNumero1" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                    <field name="COMPONENT_SELECTOR">TextBoxNumero1</field>
                    <field name="PROP">Text</field>
                  </block>
                </value>
                <value name="NUM1">
                  <block type="component_set_get" id="b_get_n2_mul">
                    <mutation component_type="TextBox" instance_name="TextBoxNumero2" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                    <field name="COMPONENT_SELECTOR">TextBoxNumero2</field>
                    <field name="PROP">Text</field>
                  </block>
                </value>
              </block>
            </value>
          </block>
        </value>
      </block>
    </statement>
  </block>

  <block type="component_event" id="b_div_click" x="30" y="540">
    <mutation component_type="Button" is_generic="false" instance_name="ButtonDivisao" event_name="Click"></mutation>
    <field name="COMPONENT_SELECTOR">ButtonDivisao</field>
    <statement name="DO">
      <block type="controls_if" id="b_if_div_zero">
        <mutation else="1"></mutation>
        <value name="IF0">
          <block type="math_compare" id="b_check_zero">
            <field name="OP">EQ</field>
            <value name="A">
              <block type="component_set_get" id="b_get_n2_div">
                <mutation component_type="TextBox" instance_name="TextBoxNumero2" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                <field name="COMPONENT_SELECTOR">TextBoxNumero2</field>
                <field name="PROP">Text</field>
              </block>
            </value>
            <value name="B">
              <block type="math_number" id="b_zero">
                <field name="NUM">0</field>
              </block>
            </value>
          </block>
        </value>
        <statement name="DO0">
          <block type="component_set_get" id="b_set_div_zero_msg">
            <mutation component_type="Label" instance_name="LabelResultado" property_name="Text" is_generic="false" get_or_set="set"></mutation>
            <field name="COMPONENT_SELECTOR">LabelResultado</field>
            <field name="PROP">Text</field>
            <value name="VALUE">
              <block type="text" id="b_err_div_zero">
                <field name="TEXT">Não é possível dividir por zero</field>
              </block>
            </value>
          </block>
        </statement>
        <statement name="ELSE">
          <block type="component_set_get" id="b_set_res_div">
            <mutation component_type="Label" instance_name="LabelResultado" property_name="Text" is_generic="false" get_or_set="set"></mutation>
            <field name="COMPONENT_SELECTOR">LabelResultado</field>
            <field name="PROP">Text</field>
            <value name="VALUE">
              <block type="text_join" id="b_join_div">
                <mutation items="2"></mutation>
                <value name="ADD0">
                  <block type="text" id="b_prefix_div">
                    <field name="TEXT">Resultado: </field>
                  </block>
                </value>
                <value name="ADD1">
                  <block type="math_division" id="b_div">
                    <value name="A">
                      <block type="component_set_get" id="b_get_n1_div">
                        <mutation component_type="TextBox" instance_name="TextBoxNumero1" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                        <field name="COMPONENT_SELECTOR">TextBoxNumero1</field>
                        <field name="PROP">Text</field>
                      </block>
                    </value>
                    <value name="B">
                      <block type="component_set_get" id="b_get_n2_div2">
                        <mutation component_type="TextBox" instance_name="TextBoxNumero2" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                        <field name="COMPONENT_SELECTOR">TextBoxNumero2</field>
                        <field name="PROP">Text</field>
                      </block>
                    </value>
                  </block>
                </value>
              </block>
            </value>
          </block>
        </statement>
      </block>
    </statement>
  </block>

  <block type="component_event" id="b_voltar_calc_click" x="30" y="780">
    <mutation component_type="Button" is_generic="false" instance_name="ButtonVoltar" event_name="Click"></mutation>
    <field name="COMPONENT_SELECTOR">ButtonVoltar</field>
    <statement name="DO">
      <block type="controls_closeScreen" id="b_close_calc"></block>
    </statement>
  </block>
</xml>"""

# --- Screen 4: IMC ---
screen4_components = [
    {
        "$Name": "LabelTitulo",
        "$Type": "Label",
        "Text": "CALCULADORA DE IMC",
        "FontSize": "24",
        "FontBold": "True",
        "TextAlignment": "1"
    },
    {
        "$Name": "LabelPeso",
        "$Type": "Label",
        "Text": "Peso (kg)",
        "FontSize": "16"
    },
    {
        "$Name": "TextBoxPeso",
        "$Type": "TextBox",
        "Hint": "Ex: 70",
        "NumbersOnly": "True",
        "Width": "-2"
    },
    {
        "$Name": "LabelAltura",
        "$Type": "Label",
        "Text": "Altura (m)",
        "FontSize": "16"
    },
    {
        "$Name": "TextBoxAltura",
        "$Type": "TextBox",
        "Hint": "Ex: 1.75",
        "NumbersOnly": "True",
        "Width": "-2"
    },
    {
        "$Name": "ButtonCalcularIMC",
        "$Type": "Button",
        "Text": "CALCULAR",
        "FontSize": "18",
        "Width": "-2"
    },
    {
        "$Name": "LabelResultadoIMC",
        "$Type": "Label",
        "Text": "Resultado:",
        "FontSize": "18",
        "FontBold": "True"
    },
    {
        "$Name": "ButtonVoltarIMC",
        "$Type": "Button",
        "Text": "VOLTAR",
        "FontSize": "18",
        "Width": "-2"
    }
]

screen4_bky = """<xml xmlns="http://www.w3.org/1999/xhtml">
  <block type="component_event" id="b_imc_calc_click" x="30" y="30">
    <mutation component_type="Button" is_generic="false" instance_name="ButtonCalcularIMC" event_name="Click"></mutation>
    <field name="COMPONENT_SELECTOR">ButtonCalcularIMC</field>
    <statement name="DO">
      <block type="controls_if" id="b_if_invalid_imc">
        <mutation else="1"></mutation>
        <value name="IF0">
          <block type="logic_operation" id="b_or_imc">
            <field name="OP">OR</field>
            <value name="A">
              <block type="math_compare" id="b_chk_peso">
                <field name="OP">LTE</field>
                <value name="A">
                  <block type="component_set_get" id="b_get_peso">
                    <mutation component_type="TextBox" instance_name="TextBoxPeso" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                    <field name="COMPONENT_SELECTOR">TextBoxPeso</field>
                    <field name="PROP">Text</field>
                  </block>
                </value>
                <value name="B">
                  <block type="math_number" id="b_zero_peso">
                    <field name="NUM">0</field>
                  </block>
                </value>
              </block>
            </value>
            <value name="B">
              <block type="math_compare" id="b_chk_altura">
                <field name="OP">LTE</field>
                <value name="A">
                  <block type="component_set_get" id="b_get_altura">
                    <mutation component_type="TextBox" instance_name="TextBoxAltura" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                    <field name="COMPONENT_SELECTOR">TextBoxAltura</field>
                    <field name="PROP">Text</field>
                  </block>
                </value>
                <value name="B">
                  <block type="math_number" id="b_zero_alt">
                    <field name="NUM">0</field>
                  </block>
                </value>
              </block>
            </value>
          </block>
        </value>
        <statement name="DO0">
          <block type="component_set_get" id="b_set_invalid_imc">
            <mutation component_type="Label" instance_name="LabelResultadoIMC" property_name="Text" is_generic="false" get_or_set="set"></mutation>
            <field name="COMPONENT_SELECTOR">LabelResultadoIMC</field>
            <field name="PROP">Text</field>
            <value name="VALUE">
              <block type="text" id="b_txt_invalid_imc">
                <field name="TEXT">Digite valores válidos</field>
              </block>
            </value>
          </block>
        </statement>
        <statement name="ELSE">
          <block type="local_declaration_statement" id="b_var_imc">
            <mutation>
              <localname name="imc"></localname>
            </mutation>
            <field name="VAR0">imc</field>
            <value name="DECL0">
              <block type="math_division" id="b_div_imc">
                <value name="A">
                  <block type="component_set_get" id="b_get_peso2">
                    <mutation component_type="TextBox" instance_name="TextBoxPeso" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                    <field name="COMPONENT_SELECTOR">TextBoxPeso</field>
                    <field name="PROP">Text</field>
                  </block>
                </value>
                <value name="B">
                  <block type="math_multiply" id="b_mult_alt">
                    <value name="NUM0">
                      <block type="component_set_get" id="b_get_alt1">
                        <mutation component_type="TextBox" instance_name="TextBoxAltura" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                        <field name="COMPONENT_SELECTOR">TextBoxAltura</field>
                        <field name="PROP">Text</field>
                      </block>
                    </value>
                    <value name="NUM1">
                      <block type="component_set_get" id="b_get_alt2">
                        <mutation component_type="TextBox" instance_name="TextBoxAltura" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                        <field name="COMPONENT_SELECTOR">TextBoxAltura</field>
                        <field name="PROP">Text</field>
                      </block>
                    </value>
                  </block>
                </value>
              </block>
            </value>
            <statement name="STACK">
              <block type="local_declaration_statement" id="b_var_class">
                <mutation>
                  <localname name="classificacao"></localname>
                </mutation>
                <field name="VAR0">classificacao</field>
                <value name="DECL0">
                  <block type="text" id="b_init_class">
                    <field name="TEXT"></field>
                  </block>
                </value>
                <statement name="STACK">
                  <block type="controls_if" id="b_if_class_imc">
                    <mutation elseif="2" else="1"></mutation>
                    <value name="IF0">
                      <block type="math_compare" id="b_lt_18_5">
                        <field name="OP">LT</field>
                        <value name="A">
                          <block type="lexical_variable_get" id="b_get_imc1">
                            <field name="VAR">imc</field>
                          </block>
                        </value>
                        <value name="B">
                          <block type="math_number" id="b_num_18_5">
                            <field name="NUM">18.5</field>
                          </block>
                        </value>
                      </block>
                    </value>
                    <statement name="DO0">
                      <block type="lexical_variable_set" id="b_set_class1">
                        <field name="VAR">classificacao</field>
                        <value name="VALUE">
                          <block type="text" id="b_txt_abaixo">
                            <field name="TEXT">Abaixo do peso</field>
                          </block>
                        </value>
                      </block>
                    </statement>
                    <value name="IF1">
                      <block type="math_compare" id="b_lt_25">
                        <field name="OP">LT</field>
                        <value name="A">
                          <block type="lexical_variable_get" id="b_get_imc2">
                            <field name="VAR">imc</field>
                          </block>
                        </value>
                        <value name="B">
                          <block type="math_number" id="b_num_25">
                            <field name="NUM">25</field>
                          </block>
                        </value>
                      </block>
                    </value>
                    <statement name="DO1">
                      <block type="lexical_variable_set" id="b_set_class2">
                        <field name="VAR">classificacao</field>
                        <value name="VALUE">
                          <block type="text" id="b_txt_normal">
                            <field name="TEXT">Faixa considerada normal</field>
                          </block>
                        </value>
                      </block>
                    </statement>
                    <value name="IF2">
                      <block type="math_compare" id="b_lt_30">
                        <field name="OP">LT</field>
                        <value name="A">
                          <block type="lexical_variable_get" id="b_get_imc3">
                            <field name="VAR">imc</field>
                          </block>
                        </value>
                        <value name="B">
                          <block type="math_number" id="b_num_30">
                            <field name="NUM">30</field>
                          </block>
                        </value>
                      </block>
                    </value>
                    <statement name="DO2">
                      <block type="lexical_variable_set" id="b_set_class3">
                        <field name="VAR">classificacao</field>
                        <value name="VALUE">
                          <block type="text" id="b_txt_sobrepeso">
                            <field name="TEXT">Sobrepeso</field>
                          </block>
                        </value>
                      </block>
                    </statement>
                    <statement name="ELSE">
                      <block type="lexical_variable_set" id="b_set_class4">
                        <field name="VAR">classificacao</field>
                        <value name="VALUE">
                          <block type="text" id="b_txt_obesidade">
                            <field name="TEXT">Obesidade</field>
                          </block>
                        </value>
                      </block>
                    </statement>
                  </block>
                  <block type="component_set_get" id="b_set_res_imc_final">
                    <mutation component_type="Label" instance_name="LabelResultadoIMC" property_name="Text" is_generic="false" get_or_set="set"></mutation>
                    <field name="COMPONENT_SELECTOR">LabelResultadoIMC</field>
                    <field name="PROP">Text</field>
                    <value name="VALUE">
                      <block type="text_join" id="b_join_imc_res">
                        <mutation items="4"></mutation>
                        <value name="ADD0">
                          <block type="text" id="b_txt_prefix_imc">
                            <field name="TEXT">Resultado: </field>
                          </block>
                        </value>
                        <value name="ADD1">
                          <block type="math_format_as_decimal" id="b_fmt_imc">
                            <value name="NUM">
                              <block type="lexical_variable_get" id="b_get_imc_final">
                                <field name="VAR">imc</field>
                              </block>
                            </value>
                            <value name="PLACES">
                              <block type="math_number" id="b_num_2_places">
                                <field name="NUM">2</field>
                              </block>
                            </value>
                          </block>
                        </value>
                        <value name="ADD2">
                          <block type="text" id="b_txt_dash">
                            <field name="TEXT"> - </field>
                          </block>
                        </value>
                        <value name="ADD3">
                          <block type="lexical_variable_get" id="b_get_class_final">
                            <field name="VAR">classificacao</field>
                          </block>
                        </value>
                      </block>
                    </value>
                  </block>
                </statement>
              </block>
            </statement>
          </block>
        </statement>
      </block>
    </statement>
  </block>

  <block type="component_event" id="b_voltar_imc_click" x="30" y="600">
    <mutation component_type="Button" is_generic="false" instance_name="ButtonVoltarIMC" event_name="Click"></mutation>
    <field name="COMPONENT_SELECTOR">ButtonVoltarIMC</field>
    <statement name="DO">
      <block type="controls_closeScreen" id="b_close_imc"></block>
    </statement>
  </block>
</xml>"""

# --- Screen 5: MÉDIA ESCOLAR ---
screen5_components = [
    {
        "$Name": "LabelTitulo",
        "$Type": "Label",
        "Text": "MÉDIA ESCOLAR",
        "FontSize": "24",
        "FontBold": "True",
        "TextAlignment": "1"
    },
    {
        "$Name": "TextBoxNota1",
        "$Type": "TextBox",
        "Hint": "Nota 1",
        "NumbersOnly": "True",
        "Width": "-2"
    },
    {
        "$Name": "TextBoxNota2",
        "$Type": "TextBox",
        "Hint": "Nota 2",
        "NumbersOnly": "True",
        "Width": "-2"
    },
    {
        "$Name": "TextBoxNota3",
        "$Type": "TextBox",
        "Hint": "Nota 3",
        "NumbersOnly": "True",
        "Width": "-2"
    },
    {
        "$Name": "ButtonCalcularMedia",
        "$Type": "Button",
        "Text": "CALCULAR MÉDIA",
        "FontSize": "18",
        "Width": "-2"
    },
    {
        "$Name": "LabelResultadoMedia",
        "$Type": "Label",
        "Text": "Resultado:",
        "FontSize": "18",
        "FontBold": "True"
    },
    {
        "$Name": "ButtonVoltarMedia",
        "$Type": "Button",
        "Text": "VOLTAR",
        "FontSize": "18",
        "Width": "-2"
    }
]

screen5_bky = """<xml xmlns="http://www.w3.org/1999/xhtml">
  <block type="component_event" id="b_media_calc_click" x="30" y="30">
    <mutation component_type="Button" is_generic="false" instance_name="ButtonCalcularMedia" event_name="Click"></mutation>
    <field name="COMPONENT_SELECTOR">ButtonCalcularMedia</field>
    <statement name="DO">
      <block type="local_declaration_statement" id="b_var_media">
        <mutation>
          <localname name="media"></localname>
        </mutation>
        <field name="VAR0">media</field>
        <value name="DECL0">
          <block type="math_division" id="b_div_media">
            <value name="A">
              <block type="math_add" id="b_sum_notes">
                <mutation items="3"></mutation>
                <value name="NUM0">
                  <block type="component_set_get" id="b_get_n1_media">
                    <mutation component_type="TextBox" instance_name="TextBoxNota1" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                    <field name="COMPONENT_SELECTOR">TextBoxNota1</field>
                    <field name="PROP">Text</field>
                  </block>
                </value>
                <value name="NUM1">
                  <block type="component_set_get" id="b_get_n2_media">
                    <mutation component_type="TextBox" instance_name="TextBoxNota2" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                    <field name="COMPONENT_SELECTOR">TextBoxNota2</field>
                    <field name="PROP">Text</field>
                  </block>
                </value>
                <value name="NUM2">
                  <block type="component_set_get" id="b_get_n3_media">
                    <mutation component_type="TextBox" instance_name="TextBoxNota3" property_name="Text" is_generic="false" get_or_set="get"></mutation>
                    <field name="COMPONENT_SELECTOR">TextBoxNota3</field>
                    <field name="PROP">Text</field>
                  </block>
                </value>
              </block>
            </value>
            <value name="B">
              <block type="math_number" id="b_num_3_media">
                <field name="NUM">3</field>
              </block>
            </value>
          </block>
        </value>
        <statement name="STACK">
          <block type="local_declaration_statement" id="b_var_status">
            <mutation>
              <localname name="status"></localname>
            </mutation>
            <field name="VAR0">status</field>
            <value name="DECL0">
              <block type="text" id="b_init_status">
                <field name="TEXT"></field>
              </block>
            </value>
            <statement name="STACK">
              <block type="controls_if" id="b_if_aprovado">
                <mutation else="1"></mutation>
                <value name="IF0">
                  <block type="math_compare" id="b_gte_6">
                    <field name="OP">GTE</field>
                    <value name="A">
                      <block type="lexical_variable_get" id="b_get_media_var1">
                        <field name="VAR">media</field>
                      </block>
                    </value>
                    <value name="B">
                      <block type="math_number" id="b_num_6">
                        <field name="NUM">6</field>
                      </block>
                    </value>
                  </block>
                </value>
                <statement name="DO0">
                  <block type="lexical_variable_set" id="b_set_status_aprovado">
                    <field name="VAR">status</field>
                    <value name="VALUE">
                      <block type="text" id="b_txt_aprovado">
                        <field name="TEXT">APROVADO</field>
                      </block>
                    </value>
                  </block>
                </statement>
                <statement name="ELSE">
                  <block type="lexical_variable_set" id="b_set_status_reprovado">
                    <field name="VAR">status</field>
                    <value name="VALUE">
                      <block type="text" id="b_txt_reprovado">
                        <field name="TEXT">REPROVADO</field>
                      </block>
                    </value>
                  </block>
                </statement>
              </block>
              <block type="component_set_get" id="b_set_res_media">
                <mutation component_type="Label" instance_name="LabelResultadoMedia" property_name="Text" is_generic="false" get_or_set="set"></mutation>
                <field name="COMPONENT_SELECTOR">LabelResultadoMedia</field>
                <field name="PROP">Text</field>
                <value name="VALUE">
                  <block type="text_join" id="b_join_media_res">
                    <mutation items="4"></mutation>
                    <value name="ADD0">
                      <block type="text" id="b_txt_prefix_media">
                        <field name="TEXT">Resultado: </field>
                      </block>
                    </value>
                    <value name="ADD1">
                      <block type="math_format_as_decimal" id="b_fmt_media">
                        <value name="NUM">
                          <block type="lexical_variable_get" id="b_get_media_var2">
                            <field name="VAR">media</field>
                          </block>
                        </value>
                        <value name="PLACES">
                          <block type="math_number" id="b_num_2_places_media">
                            <field name="NUM">2</field>
                          </block>
                        </value>
                      </block>
                    </value>
                    <value name="ADD2">
                      <block type="text" id="b_txt_dash_media">
                        <field name="TEXT"> - </field>
                      </block>
                    </value>
                    <value name="ADD3">
                      <block type="lexical_variable_get" id="b_get_status_var">
                        <field name="VAR">status</field>
                      </block>
                    </value>
                  </block>
                </value>
              </block>
            </statement>
          </block>
        </statement>
      </block>
    </statement>
  </block>

  <block type="component_event" id="b_voltar_media_click" x="30" y="450">
    <mutation component_type="Button" is_generic="false" instance_name="ButtonVoltarMedia" event_name="Click"></mutation>
    <field name="COMPONENT_SELECTOR">ButtonVoltarMedia</field>
    <statement name="DO">
      <block type="controls_closeScreen" id="b_close_media"></block>
    </statement>
  </block>
</xml>"""

def build_aia():
    aia_filename = "MultiCalcApp.aia"
    pkg_path = APP_PACKAGE.replace('.', '/')

    screens = [
        ("Screen1", "LOGIN", screen1_components, screen1_bky),
        ("Screen2", "MENU PRINCIPAL", screen2_components, screen2_bky),
        ("Screen3", "CALCULADORA", screen3_components, screen3_bky),
        ("Screen4", "CALCULADORA DE IMC", screen4_components, screen4_bky),
        ("Screen5", "MÉDIA ESCOLAR", screen5_components, screen5_bky),
    ]

    with zipfile.ZipFile(aia_filename, 'w', zipfile.ZIP_DEFLATED) as z:
        # Write project properties
        z.writestr("youngandroidproject/project.properties", PROJECT_PROPERTIES)

        # Write assets directory entry
        z.writestr("assets/", "")

        # Write each screen's .scm and .bky files
        for name, title, comps, bky_content in screens:
            scm_content = make_scm(name, title, comps)
            scm_path = f"src/{pkg_path}/{name}.scm"
            bky_path = f"src/{pkg_path}/{name}.bky"
            z.writestr(scm_path, scm_content)
            z.writestr(bky_path, bky_content)

    print(f"Successfully generated {aia_filename}")

if __name__ == "__main__":
    build_aia()
