import 'package:flutter/material.dart';
import 'package:pt_flutter_architecture/pt_flutter_architecture.dart';
import 'package:{{ package_name }}/core/architecture/mobx_obs.dart';
import 'package:{{ package_name }}/core/architecture/mobx_view.dart';
{% if include_mock %}
import 'package:{{ package_name }}/mock/{{ name_lower }}_usecase_mock.dart';
{% endif %}

import '{{ name_lower }}_viewmodel.dart';
import '{{ name_lower }}_suc.dart';
import '{{ name_lower }}_navigator.dart';

class {{ name }}Binding implements Bindings {
  {% if include_mock %}
  static const isMockEnabled = bool.fromEnvironment("mock");
  {% endif %}
  @override
  void dependencies() {
    {% if include_mock %}
    Get.put<{{ name }}SceneUseCaseType>(isMockEnabled ? {{ name }}SceneUseCaseMock() : {{ name }}SceneUseCase());
    {% else %}
    Get.put<{{ name }}SceneUseCaseType>({{ name }}SceneUseCase());
    {% endif %}
    Get.put<{{ name }}Navigator>({{ name }}Navigator());
    Get.put<{{ name }}ViewModel>({{ name }}ViewModel());
  }
}

class {{ name }}View extends MobXView<{{ name }}ViewModel> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(),
    );
  }
}
