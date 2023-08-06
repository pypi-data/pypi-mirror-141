import 'package:flutter/widgets.dart';
import 'package:mobx/mobx.dart';
import 'package:{{ package_name }}/core/architecture/mobx_ext.dart';
import 'package:{{ package_name }}/core/architecture/mobx_viewmodel.dart';

import '{{ name_lower }}_suc.dart';
import '{{ name_lower }}_navigator.dart';

class {{ name }}ViewModel extends MobXViewModel<{{ name }}SceneUseCaseType, {{ name }}Navigator> {
  /*  Variable */
  final _something = "".obs;

  /*  Input */
  late final onSomething = _onSomething;

  /*  Output */
  final something = false.obs;

  /*  Life Cycle */
  @override
  void onInit() {
    super.onInit();
    _onLoad();
  }
}

extension {{ name }}ViewModelInputs on {{ name }}ViewModel {
  void _onLoad() async {}

  void _onSomething(String value) => runInAction(() {});
}

extension {{ name }}ViewModelComputedMethods on {{ name }}ViewModel {}

extension {{ name }}ViewModelMethods on {{ name }}ViewModel {}
