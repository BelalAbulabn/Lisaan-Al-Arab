import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ChatProvider with ChangeNotifier {
  List<ChatMessage> _messages = [
    ChatMessage(msg: "السلام عليكم! معك المعتز بالله، كيف أخدمك؟", chatIndex: 1), // Initial welcome message from bot
  ];

  List<ChatMessage> get getChatList => _messages;

  int get getChatListLength => _messages.length;

  void addUserMessage({required String msg}) {
    _messages.add(ChatMessage(msg: msg, chatIndex: 0)); // chatIndex 0 for user
    notifyListeners();
  }

  Future<void> sendMessageAndGetResponse({required String msg}) async {
    print("Adding 'Typing...' placeholder");
    _messages.add(ChatMessage(msg: 'أفكر...', chatIndex: 1));
    notifyListeners(); // Update UI to show "typing..."

    try {
      // Send message to API and receive response
      String response = await ApiService.sendMessage(msg);
      print("Received response: $response");

      // Replace "typing..." with actual response
      _messages.removeLast(); // Remove the "typing..." placeholder
      _messages.add(ChatMessage(msg: response, chatIndex: 1)); // Add bot response
    } catch (e) {
      // Handle error by replacing "typing..." with an error message
      print("Error receiving response: $e");
      _messages.removeLast();
      _messages.add(ChatMessage(msg: 'Error: $e', chatIndex: 1));
    }

    print("Notifying listeners with updated messages");
    notifyListeners(); // Update UI to reflect the new message
  }
}

class ChatMessage {
  final String msg;
  final int chatIndex;

  ChatMessage({required this.msg, required this.chatIndex});
}
