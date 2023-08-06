## -*- coding: utf-8; -*-
<%inherit file="/configure.mako" />

<%def name="form_content()">

  <p class="block has-text-weight-bold is-italic">
    NB.&nbsp; Any changes made here will require an app restart!
  </p>

  <h3 class="block is-size-3">Tailbone Views</h3>

  <h4 class="block is-size-4">People</h4>
  % for key, label in view_settings['people']:
      ${self.simple_flag(key, label)}
  % endfor

  <h4 class="block is-size-4">Products</h4>
  % for key, label in view_settings['products']:
      ${self.simple_flag(key, label)}
  % endfor

  <h4 class="block is-size-4">Other</h4>
  % for key, label in view_settings['other']:
      ${self.simple_flag(key, label)}
  % endfor

</%def>

<%def name="simple_flag(key, label)">
  <b-field label="${label}" horizontal>
    <b-select name="tailbone.includes.${key}"
              v-model="simpleSettings['tailbone.includes.${key}']"
              @input="settingsNeedSaved = true">
      <option :value="null">(disabled)</option>
      <option value="${key}">${key}</option>
    </b-select>
  </b-field>
</%def>


${parent.body()}
