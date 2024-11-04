import 'package:flutter/material.dart';
import '../models/models_model.dart';
import '../services/api_service.dart';

class ModelsProvider with ChangeNotifier {
  String currentModel = 'sdaia/allam-1-13b-instruct';

  Future<List<ModelsModel>> get getAllModelsProvider {
    return ApiService.getModels();
  }

  String get getCurrentModel {
    return currentModel;
  }

  void setCurrentModel(String newModel) {
    currentModel = newModel;
    notifyListeners();
  }
}
