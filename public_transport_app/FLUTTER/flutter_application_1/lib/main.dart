import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Transport Companion App',
      theme: ThemeData(
        primarySwatch: Colors.teal,
      ),
      home: const TransportUI(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class TransportUI extends StatefulWidget {
  const TransportUI({super.key});

  @override
  _TransportUIState createState() => _TransportUIState();
}

class _TransportUIState extends State<TransportUI> with SingleTickerProviderStateMixin {
  String gpsStatus = 'Initializing…';
  double? lat;
  double? lon;
  String planResult = '';
  String payResult = '';
  final GlobalKey<AnimatedListState> _vehiclesKey = GlobalKey<AnimatedListState>();
  final List<String> vehicles = [];

  @override
  void initState() {
    super.initState();
    // Simulate loading GPS and vehicles
    Future.delayed(const Duration(seconds: 2), () {
      setState(() {
        gpsStatus = 'Active';
        lat = -37.8136;
        lon = 144.9631;
      });
      final newVehicles = ['Tram 19', 'Bus 246', 'Tram 75'];
      for (var i = 0; i < newVehicles.length; i++) {
        vehicles.add(newVehicles[i]);
        _vehiclesKey.currentState?.insertItem(
          i,
          duration: Duration(milliseconds: 300 + i * 100),
        );
      }
    });
  }

  void onPlan() {
    setState(() {
      planResult = 'Trip planned!';
    });
  }

  void onPlanLilydale() {
    setState(() {
      planResult = 'Lilydale trip planned!';
    });
  }

  void onPay() {
    setState(() {
      payResult = 'Payment successful!';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text('Transport Companion'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // GPS Status Section
              AnimatedContainer(
                duration: const Duration(milliseconds: 500),
                padding: const EdgeInsets.all(8),
                margin: const EdgeInsets.only(bottom: 12),
                decoration: BoxDecoration(
                  color: gpsStatus == 'Active'
                      ? Colors.greenAccent.shade100
                      : const Color(0xFFE0FFE0),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'GPS Status',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 4),
                    Row(
                      children: [
                        Text(gpsStatus),
                        const Spacer(),
                        Text("Lat: ${lat?.toStringAsFixed(4) ?? '--'}"),
                        const SizedBox(width: 10),
                        Text("Lon: ${lon?.toStringAsFixed(4) ?? '--'}"),
                      ],
                    ),
                  ],
                ),
              ),
              // Nearby Vehicles Section
              Container(
                height: 200,
                margin: const EdgeInsets.only(bottom: 12),
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Nearby Vehicles',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 4),
                    Expanded(
                      child: AnimatedList(
                        key: _vehiclesKey,
                        initialItemCount: vehicles.length,
                        itemBuilder: (context, index, animation) {
                          return FadeTransition(
                            opacity: animation,
                            child: ListTile(
                              leading: const Icon(Icons.directions_transit),
                              title: Text(vehicles[index]),
                            ),
                          );
                        },
                      ),
                    ),
                  ],
                ),
              ),
              // Trip Planner Section
              AnimatedContainer(
                duration: const Duration(milliseconds: 500),
                padding: const EdgeInsets.all(8),
                margin: const EdgeInsets.only(bottom: 12),
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Plan Your Trip',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 4),
                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            decoration: const InputDecoration(hintText: 'Enter destination'),
                          ),
                        ),
                        const SizedBox(width: 8),
                        ElevatedButton(onPressed: onPlan, child: const Text('Plan')),
                      ],
                    ),
                    const SizedBox(height: 8),
                    ElevatedButton(onPressed: onPlanLilydale, child: const Text('Quick Lilydale Trip')),
                    const SizedBox(height: 8),
                    AnimatedOpacity(
                      opacity: planResult.isEmpty ? 0 : 1,
                      duration: const Duration(milliseconds: 300),
                      child: Text(planResult),
                    ),
                  ],
                ),
              ),
              // Payment Section
              AnimatedContainer(
                duration: const Duration(milliseconds: 500),
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Make Payment',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 4),
                    Row(
                      children: [
                        Expanded(child: TextField(decoration: const InputDecoration(hintText: 'Trip ID'))),
                        const SizedBox(width: 8),
                        Expanded(child: TextField(decoration: const InputDecoration(hintText: 'Amount'), keyboardType: TextInputType.number)),
                        const SizedBox(width: 8),
                        ElevatedButton(onPressed: onPay, child: const Text('Pay')),
                      ],
                    ),
                    const SizedBox(height: 8),
                    AnimatedOpacity(
                      opacity: payResult.isEmpty ? 0 : 1,
                      duration: const Duration(milliseconds: 300),
                      child: Text(payResult),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}