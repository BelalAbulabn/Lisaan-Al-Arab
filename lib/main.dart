import 'package:chat_gpt/provider/chat_provider.dart';
import 'package:chat_gpt/provider/models_provider.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'constants/constants.dart';
import 'screens/chat_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => ModelsProvider()),
        ChangeNotifierProvider(create: (_) => ChatProvider()),
      ],
      child: MaterialApp(
        title: 'Allam',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          scaffoldBackgroundColor: scaffoldBackgroundColor,
          appBarTheme: AppBarTheme(color: cardColor),
        ),
        home: const ChatScreen(),
        locale: const Locale('ar'), // Set Arabic locale for RTL support
        builder: (context, child) {
          return Directionality(
            textDirection: TextDirection.rtl, // Set global RTL direction
            child: child!,
          );
        },
      ),
    );
  }
}
