import 'package:flutter/material.dart';
import '../models/chat_model.dart';
import '../services/api_service.dart';

class ChatProvider with ChangeNotifier {
  final List<ChatModel> _chatList = [];
  List<ChatModel> get getChatList => _chatList;

  int get getChatListLength => _chatList.length;

  void addUserMessage({required String msg}) {
    _chatList.add(ChatModel(msg: msg, chatIndex: 0));
    notifyListeners();
  }

  Future<void> sendMessageAndGetResponse({required String msg}) async {
    try {
      // Get response from API
      String response = await ApiService.sendMessage(message: msg);

      // Add bot response
      _chatList.add(ChatModel(msg: response, chatIndex: 1));
      notifyListeners();
    } catch (error) {
      // Handle errors
      _chatList.add(ChatModel(
        msg: 'An error occurred: $error',
        chatIndex: 1,
      ));
      notifyListeners();
    }
  }
}
