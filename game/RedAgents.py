from typing import List, Tuple, Union, Optional
from .ImageRect import ImageRect
from .SharedKnowledge import SharedKnowledge
import pygame
import os
import math
import random
import numpy as np
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Предварительные объявления для типизации
class BlueMeleeAgent:
    pass

class BlueBase:
    pass

class RedBase:
    pass

class Obstacle:
    pass

class RedMeleeAgent:
    shared_knowledge = SharedKnowledge()

    def __init__(self, x: int, y: int):
        self.image = ImageRect(x, y, os.path.join("game", "RedMeleeAgent.png"))
        self.speed = 2
        self.max_health = 2500  # Увеличено в 5 раз
        self.health = self.max_health
        self.damage = 20
        self.base_damage = 10  # Урон по базе
        self.target: Optional[Tuple[int, int]] = None
        self.last_attack_time = 0
        self.attack_cooldown = 1000
        self.attack_range = 70
        self.defending_base = False
        self.reached_initial_position = False
        self.initial_position = (x, y)
        self.personal_obstacles = set()
        self.id = id(self)

    def is_visible(self, start: Tuple[int, int], end: Tuple[int, int], obstacles: List[Obstacle]) -> bool:
        """Проверяет, вид��ма ли конечная точка из начальной точки."""
        return True  # Убираем проверку на видимость через препятствия

    def find_nearest_enemy(self, blue_agents: List[BlueMeleeAgent], obstacles: List[Obstacle]) -> Tuple[Optional[BlueMeleeAgent], float]:
        if not blue_agents:
            return None, float('inf')

        agent_positions = np.array([agent.image.rect.center for agent in blue_agents if agent.is_alive()])
        my_position = np.array(self.image.rect.center)

        distances = np.linalg.norm(agent_positions - my_position, axis=1)
        visible_mask = np.ones(len(agent_positions), dtype=bool)  # Все раги видимы

        if not np.any(visible_mask):
            return None, float('inf')

        visible_distances = distances[visible_mask]
        nearest_index = np.argmin(visible_distances)
        nearest_agent = [agent for agent in blue_agents if agent.is_alive()][np.where(visible_mask)[0][nearest_index]]

        return nearest_agent, visible_distances[nearest_index]

    def attack(self, target: Union[BlueMeleeAgent, BlueBase]):
        if target.health <= 0:
            self.target = None
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            target.health -= self.damage
            target.health = max(0, target.health)
            self.last_attack_time = current_time

    def is_base_under_attack(self, red_base: RedBase, blue_agents: List[BlueMeleeAgent], obstacles: List[Obstacle]) -> bool:
        return any(agent.is_alive() and red_base.rect.colliderect(agent.image.rect) for agent in blue_agents)

    def choose_action(self, state, red_base, blue_agents, obstacles):
        # Пример простого выбора действия
        if self.is_base_under_attack(red_base, blue_agents, obstacles):
            return 'defend'
        elif self.health < self.max_health * 0.3:
            return 'retreat'
        else:
            return 'attack'

    def perform_action(self, action, blue_base, red_base, blue_agents, red_agents, obstacles):
        if action == 'attack':
            self.move_towards_enemy_base(blue_base)
            self.attack_base(blue_base)
        elif action == 'defend':
            self.defend_base(red_base, blue_agents)
        elif action == 'retreat':
            self.retreat([(red_base.rect.x, red_base.rect.y)])
        # Добавьте другие действия по мере необходимости

    def update(self, blue_base, red_base, blue_agents, red_agents, obstacles):
        if not self.is_alive():
            return
        state = self.get_state(blue_base, red_base, blue_agents, red_agents, obstacles)
        action = self.choose_action(state, red_base, blue_agents, obstacles)
        self.perform_action(action, blue_base, red_base, blue_agents, red_agents, obstacles)

    def get_state(self, blue_base, red_base, blue_agents, red_agents, obstacles):
        # Преобразование текущего состояния в вектор признаков
        # Например, расстояние до базы, количество врагов поблизости и т.д.
        return []

    def move_towards_enemy_base(self, blue_base: BlueBase):
        target_position = np.array(blue_base.rect.center)
        my_position = np.array(self.image.rect.center)
        direction = target_position - my_position
        distance = np.linalg.norm(direction)

        if distance > self.speed:
            normalized_direction = direction / distance
            new_position = my_position + self.speed * normalized_direction

            # Проверка на выход за пределы экрана
            new_position[0] = np.clip(new_position[0], 0, SCREEN_WIDTH - 1)
            new_position[1] = np.clip(new_position[1], 0, SCREEN_HEIGHT - 1)

            self.image.rect.center = tuple(new_position)

    def move_towards_target(self):
        if not self.target:
            return

        my_position = np.array(self.image.rect.center)
        target_position = np.array(self.target)
        direction = target_position - my_position
        distance = np.linalg.norm(direction)

        if distance > self.speed:
            normalized_direction = direction / distance
            new_position = my_position + self.speed * normalized_direction

            # Проверка на выход за пределы экрана
            new_position[0] = np.clip(new_position[0], 0, SCREEN_WIDTH - 1)
            new_position[1] = np.clip(new_position[1], 0, SCREEN_HEIGHT - 1)

            self.image.rect.center = tuple(new_position)

    def share_enemy_positions(self, blue_agents: List[BlueMeleeAgent]):
        for enemy in blue_agents:
            if enemy.is_alive():
                self.shared_knowledge.update_enemy_position(id(enemy), enemy.image.rect.center)

    def defend_base(self, base, enemies):
        base_center = np.array(base.rect.center)
        my_pos = np.array(self.image.rect.center)

        # Держаться на определенном расстоянии от базы
        ideal_distance = 100
        to_base = base_center - my_pos
        dist_to_base = np.linalg.norm(to_base)

        if dist_to_base > ideal_distance:
            self.move_towards(base_center)
        elif dist_to_base < ideal_distance - 10 and dist_to_base != 0:
            # Проверяем, что dist_to_base не равен нулю, чтобы избежать деления на ноль
            self.move_towards(tuple(my_pos - to_base / dist_to_base * 10))

        # Атаковать ближайшего врага в зоне защиты
        for enemy in enemies:
            if np.linalg.norm(np.array(enemy.image.rect.center) - base_center) < ideal_distance + 50:
                self.attack(enemy)
                break

    def group_behavior(self, allies):
        center = np.mean([ally.image.rect.center for ally in allies], axis=0)
        self.move_towards(center)

        # Избегание столкновений
        for ally in allies:
            if ally != self:
                diff = np.array(self.image.rect.center) - np.array(ally.image.rect.center)
                dist = np.linalg.norm(diff)
                if dist < 30:  # Минимальное расстояние между агентами
                    self.image.rect.center = tuple(np.array(self.image.rect.center) + diff / dist * 5)

    def evade(self, threats):
        evasion_vector = np.zeros(2)
        for threat in threats:
            diff = np.array(self.image.rect.center) - np.array(threat.image.rect.center)
            dist = np.linalg.norm(diff)
            if dist < 100:  # Расстояние, на котором начинаем уклоняться
                evasion_vector += diff / (dist ** 2)

        if np.linalg.norm(evasion_vector) > 0:
            evasion_vector = evasion_vector / np.linalg.norm(evasion_vector) * self.speed
            new_pos = np.array(self.image.rect.center) + evasion_vector

            # Ограничиваем новую позицию в пределах экрана
            new_pos = np.clip(new_pos, [0, 0], [SCREEN_WIDTH, SCREEN_HEIGHT])

            # Преобразуем в целые числа перед присваиванием
            self.image.rect.center = tuple(map(int, new_pos))

    def get_directions_to_enemies(self, blue_agents: List[BlueMeleeAgent]) -> List[np.ndarray]:
        my_position = np.array(self.image.rect.center)
        directions = [np.array(agent.image.rect.center) - my_position for agent in blue_agents if agent.is_alive()]
        return [direction / np.linalg.norm(direction) for direction in directions]

    def get_distances_to_enemies(self, blue_agents: List[BlueMeleeAgent]) -> List[float]:
        my_position = np.array(self.image.rect.center)
        return [np.linalg.norm(np.array(agent.image.rect.center) - my_position) for agent in blue_agents if agent.is_alive()]

    def get_directions_to_allies(self, red_agents: List['RedMeleeAgent']) -> List[np.ndarray]:
        my_position = np.array(self.image.rect.center)
        directions = [np.array(agent.image.rect.center) - my_position for agent in red_agents if agent.is_alive() and agent != self]
        return [direction / np.linalg.norm(direction) for direction in directions]

    def get_distances_to_allies(self, red_agents: List['RedMeleeAgent']) -> List[float]:
        my_position = np.array(self.image.rect.center)
        return [np.linalg.norm(np.array(agent.image.rect.center) - my_position) for agent in red_agents if agent.is_alive() and agent != self]

    def get_sensor_ranges(self) -> List[float]:
        # Пример: все датчики имеют одинаковую дальность
        return [self.attack_range] * len(self.get_directions_to_enemies([]))  # или другое значение

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image.image, self.image.rect)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen: pygame.Surface):
        bar_width = self.image.rect.width
        bar_height = 5
        bar_position = (self.image.rect.x, self.image.rect.y - 10)

        health_width = int(self.health / self.max_health * bar_width)
        pygame.draw.rect(screen, (0, 255, 0), (*bar_position, health_width, bar_height))

    def is_alive(self) -> bool:
        return self.health > 0

    def move_towards(self, target):
        direction = np.array(target) - np.array(self.image.rect.center)
        distance = np.linalg.norm(direction)

        if distance <= self.speed:
            new_position = target
        else:
            normalized_direction = direction / distance
            new_position = np.array(self.image.rect.center) + self.speed * normalized_direction

        # Ограничиваем новую позицию в пределах экрана
        new_position = np.clip(new_position, [0, 0], [SCREEN_WIDTH, SCREEN_HEIGHT])

        # Преобразуем в целы�� числа перед присваиванием
        self.image.rect.center = tuple(map(int, new_position))

        return np.array_equal(new_position, target)

    def scout(self, unexplored_areas: List[Tuple[int, int]]):
        """
        Разведка: исследование неизвестных областей карты.
        """
        if not hasattr(self, 'current_scout_target'):
            self.current_scout_target = random.choice(unexplored_areas)

        if self.move_towards(self.current_scout_target):
            unexplored_areas.remove(self.current_scout_target)
            if unexplored_areas:
                self.current_scout_target = random.choice(unexplored_areas)
            else:
                self.current_scout_target = None

        # Здесь можно добавить логику обнаружения врагов или ресурсов

    def set_ambush(self, strategic_points: List[Tuple[int, int]]):
        """
        Засада: вбор стратегической точки для засады.
        """
        if not hasattr(self, 'ambush_point'):
            self.ambush_point = random.choice(strategic_points)

        self.move_towards(self.ambush_point)

        # Здесь можно добавить логику ожидания и внезапной атаки

    def retreat(self, safe_locations: List[Tuple[int, int]]):
        """
        Отступление: стратегическое отступление при низком здоровье или перед превосходящими силами.
        """
        if self.health < self.max_health * 0.3:  # Отступаем при здоровье ниже 30%
            nearest_safe_location = min(safe_locations, key=lambda loc: np.linalg.norm(np.array(loc) - np.array(self.image.rect.center)))
            self.move_towards(nearest_safe_location)

    def form_formation(self, allies: List['RedMeleeAgent'], formation_type: str):
        """
        Формирование строя: выстраивание в определенные формации.
        """
        if formation_type == "line":
            # Пример линейного построения
            center = np.mean([ally.image.rect.center for ally in allies], axis=0)
            direction = np.array([1, 0])  # Направление линии
            spacing = 40  # Расстояние между агентами

            position = center + (len(allies) // 2 - allies.index(self)) * spacing * direction
            self.move_towards(tuple(position))

        elif formation_type == "circle":
            # Пример кругового построения
            center = np.mean([ally.image.rect.center for ally in allies], axis=0)
            angle = 2 * np.pi * allies.index(self) / len(allies)
            radius = 50  # Радиус круга
            position = center + radius * np.array([np.cos(angle), np.sin(angle)])
            self.move_towards(tuple(position))

        # Можно добавить другие типы формаций

    def attack_base(self, enemy_base):
        if pygame.Rect.colliderect(self.image.rect, enemy_base.rect):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_attack_time >= self.attack_cooldown:
                enemy_base.health -= self.base_damage
                enemy_base.health = max(0, enemy_base.health)
                self.last_attack_time = current_time
