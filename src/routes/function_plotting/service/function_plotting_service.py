from typing import List, Tuple
import numpy as np
import numexpr as ne
import sympy as sp
import re
import zlib
import base64
import msgpack
from scipy import optimize


class FunctionPlottingService : 

    def _convert_to_python_expr(self, expr: str) -> str:
        expr = expr.replace('^', '**')
        
        expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
        
        expr = re.sub(r'(\d)(\()', r'\1*\2', expr)
        
        expr = re.sub(r'([a-zA-Z])(\()', r'\1*\2', expr)
        
        return expr

    def _find_critical_points(self,function_str: str, x_min: float, x_max: float) -> List[float]:
        x = sp.symbols('x')
        try:
            expr = sp.sympify(function_str)
            deriv = sp.diff(expr, x)
            second_deriv = sp.diff(expr, x, 2) 
            f_prime = sp.lambdify(x, deriv, "numpy")
            f_double = sp.lambdify(x, second_deriv, "numpy")
            critical_points = set()
            x_samples = np.linspace(x_min, x_max, 100)
            y_prime_samples = f_prime(x_samples)
            sign_changes = np.where(np.diff(np.signbit(y_prime_samples)))[0]   
            for i in sign_changes:
                left, right = x_samples[i], x_samples[i + 1]
                x0 = (left + right) / 2  
                
                try:
                    result = optimize.newton(f_prime, x0, fprime=f_double, maxiter=50, tol=1e-10)   
                    if x_min <= result <= x_max and abs(f_prime(result)) < 1e-8:
                        critical_points.add(round(result, 10))  
                    else:
                        result = optimize.root_scalar(f_prime, bracket=[left, right])
                        if result.converged:
                            critical_points.add(round(result.root, 10))
                except:
                    try:
                        result = optimize.root_scalar(f_prime, bracket=[left, right])
                        if result.converged:
                            critical_points.add(round(result.root, 10))
                    except:
                        pass  
            
            additional_starts = np.linspace(x_min, x_max, 10)
            for x0 in additional_starts:
                try:
                    result = optimize.newton(f_prime, x0, fprime=f_double, maxiter=50, tol=1e-10)
                    if x_min <= result <= x_max and abs(f_prime(result)) < 1e-8:
                        critical_points.add(round(result, 10))
                except:
                    pass
            
            return sorted(list(critical_points))
        except:
            return []
    
    def _find_inflection_points(self,function_str: str, x_min: float, x_max: float) -> List[float]:
        x = sp.symbols('x')
        try:
            expr = sp.sympify(function_str)
            second_deriv = sp.diff(expr, x, 2)
            
            f_double_prime = sp.lambdify(x, second_deriv, "numpy")
            
            inflection_points = []
            
            x_samples = np.linspace(x_min, x_max, 100)
            y_double_prime_samples = f_double_prime(x_samples)
            
            sign_changes = np.where(np.diff(np.signbit(y_double_prime_samples)))[0]
            
            for i in sign_changes:
                left, right = x_samples[i], x_samples[i + 1]
                try:
                    result = optimize.root_scalar(f_double_prime, bracket=[left, right])
                    if result.converged:
                        inflection_points.append(result.root)
                except:
                    pass  
            
            return inflection_points
        except:
            return []

    def _detect_asymptotes(self,function_str: str, x_min: float, x_max: float) -> List[float]:
        try:
            x_test = np.linspace(x_min, x_max, 500)
            y_test = ne.evaluate(function_str, {'x': x_test})
            
            y_diff = np.abs(np.diff(y_test))
            threshold = np.nanmean(y_diff) + 5 * np.nanstd(y_diff)
            potential_asymptotes = np.where(y_diff > threshold)[0]
            
            asymptotes = []
            for idx in potential_asymptotes:
                x_value = (x_test[idx] + x_test[idx + 1]) / 2
                asymptotes.append(x_value)
            
            return asymptotes
        except:
            return []

    def adaptive_sampling(self,function_str: str, x_min: float, x_max: float, 
                        precision: int = 100, max_points: int = 3000) -> Tuple[np.ndarray, np.ndarray, list[list[float]], list[list[float]]]:
        x_initial = np.linspace(x_min, x_max, precision)
        
        critical_points = self._find_critical_points(function_str, x_min, x_max)
        inflection_points = self._find_inflection_points(function_str, x_min, x_max)
        asymptotes = self._detect_asymptotes(function_str, x_min, x_max)

        critical_data_points : list[list[float]] = []
        inflection_data_points : list[list[float]] = []
        for point in critical_points:
            if x_min <= point <= x_max:
                critical_data_points.append([point, ne.evaluate(function_str, {'x': point}).tolist()])
        for point in inflection_points:
            if x_min <= point <= x_max:
                inflection_data_points.append([point, ne.evaluate(function_str, {'x': point})])

        
        special_points = []
        special_points.extend(critical_points)
        special_points.extend(inflection_points)
        
        for asym in asymptotes:
            delta = (x_max - x_min) / 500  
            special_points.extend([asym - delta, asym + delta])
        
        x_values = np.sort(np.append(x_initial, special_points))
        
        y_values = ne.evaluate(function_str, {'x': x_values})
        
        if  len(x_values) > max_points:
            
            
            keep_mask = np.zeros(len(x_values), dtype=bool)
                
            for point in special_points:
                idx = np.abs(x_values - point).argmin()
                keep_mask[idx] = True
                
            keep_mask[0] = keep_mask[-1] = True
                
            remaining_indices = np.where(~keep_mask)[0]
            remaining_indices = remaining_indices[1:-1]  
            
            importance = np.zeros(len(remaining_indices))
            for i, idx in enumerate(remaining_indices):
                if idx > 0 and idx < len(x_values) - 1:
                    left_slope = (y_values[idx] - y_values[idx-1]) / (x_values[idx] - x_values[idx-1])
                    right_slope = (y_values[idx+1] - y_values[idx]) / (x_values[idx+1] - x_values[idx])
                    importance[i] = abs(right_slope - left_slope)
                
            important_indices = remaining_indices[np.argsort(importance)[::-1]]
            points_to_add = min(len(important_indices), max_points - np.sum(keep_mask))
            keep_mask[important_indices[:points_to_add]] = True
                
            x_values = x_values[keep_mask]
            y_values = y_values[keep_mask]
        
        final_x, final_y = [], []
        for i in range(len(x_values) - 1):
            final_x.append(x_values[i])
            final_y.append(y_values[i])
            
            if abs(y_values[i+1] - y_values[i]) > 10 * np.nanstd(y_values):
                intermediate_x = np.linspace(x_values[i], x_values[i+1], 5)[1:-1]
                intermediate_y = ne.evaluate(function_str, {'x': intermediate_x})
                final_x.extend(intermediate_x)
                final_y.extend(intermediate_y)
        
        final_x.append(x_values[-1])
        final_y.append(y_values[-1])
        
        return np.array(final_x), np.array(final_y), critical_data_points, inflection_data_points

    def generate_plot_data(self, function : str, lower_bound : float, upper_bound : float, precision : int , max_points : int ) -> dict:
        try:
            lower = lower_bound if lower_bound is not None else -10
            upper = upper_bound if upper_bound is not None else 10
            if lower >= upper:
                raise ValueError("Lower bound must be less than upper bound.")
            
            function = self._convert_to_python_expr(function)
            
            x, y, critical_points, inflection_points = self.adaptive_sampling(
                function, 
                lower, 
                upper,
                precision=precision,
                max_points=max_points
            )
            
            mask = np.isfinite(y)
            x = x[mask]
            y = y[mask]
            
            unique_mask = np.append(True, np.diff(x) > 1e-10)
            x = x[unique_mask]
            y = y[unique_mask]
            
            data = {'x': x.tolist(), 'y': y.tolist()}
            
            packed_data = msgpack.packb(data)
            compressed_data = zlib.compress(packed_data)
            
            return {
                "data": base64.b64encode(compressed_data).decode('utf-8'),
                "points_count": len(x),
                "critical_points": critical_points,
                "inflection_points": inflection_points
            }
        
        except Exception as e:
            raise Exception(f"Error processing function '{function}': {str(e)}")
        
