class ModelsModel {
  final String id;
  final String name;

  ModelsModel({required this.id, required this.name});

  factory ModelsModel.fromJson(Map<String, dynamic> json) {
    return ModelsModel(
      id: json['metadata']['id'] ?? '',
      name: json['metadata']['name'] ?? '',
    );
  }
}
