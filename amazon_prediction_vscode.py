# Simulación del Sistema de Predicción de Amazon - VSCode Version
# Ejecutar con: python amazon_prediction_vscode.py

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

class AmazonDeliveryPredictor:
    def __init__(self):
        self.centers = {
            'Madrid_Norte': {'capacity': 0.8, 'distance_factor': 1.2},
            'Madrid_Sur': {'capacity': 0.75, 'distance_factor': 1.0},
            'Madrid_Este': {'capacity': 0.9, 'distance_factor': 1.1}
        }
        
        # Factores de tráfico por hora
        self.traffic_factors = {
            'morning_rush': (7, 10, 1.3),  # 7-10 AM, factor 1.3
            'afternoon': (10, 16, 1.0),    # 10-16 PM, factor 1.0
            'evening_rush': (16, 20, 1.4), # 16-20 PM, factor 1.4
            'night': (20, 7, 0.8)          # 20-7 PM, factor 0.8
        }
    
    def get_traffic_factor(self, hour):
        """Obtiene el factor de tráfico según la hora"""
        for period, (start, end, factor) in self.traffic_factors.items():
            if period == 'night':
                if hour >= start or hour < end:
                    return factor
            else:
                if start <= hour < end:
                    return factor
        return 1.0
    
    def select_optimal_center(self, address):
        """Selecciona el centro logístico óptimo"""
        # Simulación: Madrid Sur es el más cercano a Gran Vía
        return 'Madrid_Sur'
    
    def calculate_delivery_time(self, order_time, center, traffic_factor):
        """Calcula el tiempo de entrega estimado"""
        base_time = 30  # minutos base
        center_factor = self.centers[center]['distance_factor']
        capacity_factor = 1 + (self.centers[center]['capacity'] - 0.5) * 0.5
        
        total_time = base_time * center_factor * traffic_factor * capacity_factor
        return int(total_time)
    
    def predict_delivery(self, order_data):
        """Predice la entrega del pedido"""
        order_time = datetime.strptime(order_data['hora'], '%H:%M')
        hour = order_time.hour
        
        # Obtener factores
        traffic_factor = self.get_traffic_factor(hour)
        optimal_center = self.select_optimal_center(order_data['direccion'])
        
        # Calcular tiempo de entrega
        delivery_minutes = self.calculate_delivery_time(
            order_time, optimal_center, traffic_factor
        )
        
        # Calcular fecha y hora de entrega
        delivery_date = datetime.now() + timedelta(days=1)
        delivery_start = delivery_date.replace(hour=16, minute=0)
        delivery_end = delivery_date.replace(hour=18, minute=0)
        
        return {
            'centro_logistico': optimal_center,
            'tiempo_estimado_minutos': delivery_minutes,
            'fecha_entrega': delivery_date.strftime('%Y-%m-%d'),
            'franja_horaria': f"{delivery_start.strftime('%H:%M')} - {delivery_end.strftime('%H:%M')}",
            'factor_trafico': traffic_factor,
            'capacidad_centro': self.centers[optimal_center]['capacity']
        }

def demo_interactivo():
    """Demo interactivo para VSCode"""
    print("🚀 SIMULACIÓN AMAZON - PREDICCIÓN DE ENTREGAS")
    print("=" * 50)
    
    predictor = AmazonDeliveryPredictor()
    
    # Ejemplo principal
    pedido_ejemplo = {
        'hora': '10:35',
        'producto': 'libro',
        'direccion': 'Calle Gran Vía, 123, Madrid',
        'tipo_entrega': 'Prime'
    }
    
    resultado = predictor.predict_delivery(pedido_ejemplo)
    
    print("🛒 PREDICCIÓN DE ENTREGA AMAZON")
    print("=" * 40)
    print(f"📦 Producto: {pedido_ejemplo['producto']}")
    print(f"📍 Dirección: {pedido_ejemplo['direccion']}")
    print(f"🕐 Hora de pedido: {pedido_ejemplo['hora']}")
    print()
    print("🤖 ANÁLISIS DE IA:")
    print(f"🏢 Centro logístico: {resultado['centro_logistico']}")
    print(f"📊 Capacidad del centro: {resultado['capacidad_centro']:.1%}")
    print(f"🚦 Factor de tráfico: {resultado['factor_trafico']:.1f}x")
    print(f"⏱️ Tiempo estimado: {resultado['tiempo_estimado_minutos']} minutos")
    print()
    print("📅 RESULTADO FINAL:")
    print(f"📦 Tu pedido llegará el {resultado['fecha_entrega']}")
    print(f"🕐 Entre las {resultado['franja_horaria']}")
    print()
    print("✅ Predicción generada exitosamente!")
    
    # Análisis de diferentes horarios
    print("\n" + "=" * 50)
    print("📊 ANÁLISIS DE DIFERENTES HORARIOS")
    print("=" * 50)
    
    horas_analisis = [
        ('08:30', 'Hora punta mañana'),
        ('12:00', 'Mediodía'),
        ('14:15', 'Tarde normal'),
        ('18:45', 'Hora punta tarde'),
        ('22:00', 'Noche')
    ]
    
    for hora, descripcion in horas_analisis:
        pedido_test = pedido_ejemplo.copy()
        pedido_test['hora'] = hora
        
        resultado_test = predictor.predict_delivery(pedido_test)
        
        print(f"\n🕐 {descripcion} ({hora}):")
        print(f"   🚦 Factor tráfico: {resultado_test['factor_trafico']:.1f}x")
        print(f"   ⏱️ Tiempo estimado: {resultado_test['tiempo_estimado_minutos']} min")
        print(f"   📅 Entrega: {resultado_test['franja_horaria']}")
    
    # Estadísticas del sistema
    print("\n" + "=" * 50)
    print("📈 ESTADÍSTICAS DEL SISTEMA")
    print("=" * 50)
    
    tiempos = []
    factores = []
    
    for hora, _ in horas_analisis:
        pedido_stat = pedido_ejemplo.copy()
        pedido_stat['hora'] = hora
        resultado_stat = predictor.predict_delivery(pedido_stat)
        tiempos.append(resultado_stat['tiempo_estimado_minutos'])
        factores.append(resultado_stat['factor_trafico'])
    
    print(f"⏱️ Tiempo promedio: {np.mean(tiempos):.1f} minutos")
    print(f"📊 Factor tráfico promedio: {np.mean(factores):.2f}x")
    print(f"🚀 Tiempo mínimo: {min(tiempos)} minutos")
    print(f"🐌 Tiempo máximo: {max(tiempos)} minutos")

if __name__ == "__main__":
    demo_interactivo()
