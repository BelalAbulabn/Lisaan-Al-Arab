import 'package:animated_text_kit/animated_text_kit.dart';
import 'package:chat_gpt/constants/constants.dart';
import 'package:chat_gpt/provider/models_provider.dart';
import 'package:chat_gpt/services/assets_manager.dart';
import 'package:chat_gpt/widgets/chat_widget.dart';
import 'package:chat_gpt/widgets/text_widget.dart';
import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:provider/provider.dart';

import '../provider/chat_provider.dart';
import '../services/services.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  bool _isTyping = false;

  late final TextEditingController _textEditingController;
  late final ScrollController _listScrollController;
  late final FocusNode _focusNode;

  @override
  void initState() {
    _textEditingController = TextEditingController();
    _textEditingController.addListener(() {
      setState(() {}); // Rebuild to apply the text direction dynamically
    });
    _listScrollController = ScrollController();
    _focusNode = FocusNode();
    super.initState();
  }

  @override
  void dispose() {
    _textEditingController.dispose();
    _listScrollController.dispose();
    _focusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final modelProvider = Provider.of<ModelsProvider>(context, listen: false);
    final chatProvider = Provider.of<ChatProvider>(context, listen: false);

    return Scaffold(
      appBar: AppBar(
        title: const Text('لسان العرب',
            style: TextStyle(color: Colors.white)),
        leading: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Image.asset(AssetsManager.openaiLogo),
        ),
        actions: [
          IconButton(
            onPressed: () async {
              await Services.showModelSheet(context: context);
            },
            icon: const Icon(Icons.more_vert, color: Colors.white),
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            Flexible(
              child: Consumer<ChatProvider>(
                builder: (context, chatProvider, child) {
                  return ListView.builder(
                    controller: _listScrollController,
                    itemCount: chatProvider.getChatListLength,
                    itemBuilder: (context, index) {
                      final message = chatProvider.getChatList[index];
                      return ChatWidget(
                        msg: message.msg,
                        chatIndex: message.chatIndex,
                      );
                    },
                  );
                },
              ),
            ),
            if (_isTyping) ...[
              const SpinKitThreeBounce(
                color: Colors.white,
                size: 18,
              ),
            ],
            const SizedBox(height: 15),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _textEditingController,
                      focusNode: _focusNode,
                      style: const TextStyle(color: Colors.white),
                      textDirection: isArabic(_textEditingController.text)
                          ? TextDirection.rtl
                          : TextDirection.rtl,
                      decoration: InputDecoration(
                        hintText: 'أدخل الرسالة...',
                        hintStyle: const TextStyle(color: Colors.grey),
                        filled: true,
                        fillColor: cardColor,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(15),
                          borderSide: BorderSide.none,
                        ),
                      ),
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.send, color: Colors.white),
                    onPressed: () async {
                      await _sendMessageFCT(
                        modelProvider: modelProvider,
                        chatProvider: chatProvider,
                      );
                    },
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }


  void scrollListToEnd() {
    _listScrollController.animateTo(
      _listScrollController.position.maxScrollExtent,
      duration: const Duration(seconds: 1),
      curve: Curves.ease,
    );
  }

  Future<void> _sendMessageFCT({
    required ModelsProvider modelProvider,
    required ChatProvider chatProvider,
  }) async {
    final String msg = _textEditingController.text;

    setState(() {
      _isTyping = true;
      chatProvider.addUserMessage(msg: msg);
      _textEditingController.clear();
      _focusNode.unfocus();
    });
    print("Started typing...");

    try {
      await chatProvider.sendMessageAndGetResponse(msg: msg);
    } catch (error) {
      errorSnackBar(errMsg: error.toString());
      print('Error in _sendMessageFCT: $error');
    } finally {
      setState(() {
        scrollListToEnd();
        _isTyping = false; // Reset typing indicator here
      });
      print("Stopped typing...");
    }
  }


  void errorSnackBar({required String errMsg}) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: TextWidget(label: errMsg),
        backgroundColor: Colors.red,
        behavior: SnackBarBehavior.floating,
        padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 30),
      ),
    );
  }
}

bool isArabic(String text) {
  final arabicRegExp = RegExp(r'[\u0600-\u06FF]');
  return arabicRegExp.hasMatch(text);
}
