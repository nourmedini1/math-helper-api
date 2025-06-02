from typing import List, Tuple, Callable, Optional, Dict, Any, Union
import numpy as np
import sympy as sp
import re
import zlib
import base64
import msgpack
from scipy import optimize
from dataclasses import dataclass


@dataclass
class FunctionData:
    func: Callable
    expr: sp.Expr
    x_symbol: sp.Symbol


class FunctionPlottingService:

    def _convert_to_python_expr(self, expr: str) -> str:
        expr = expr.replace('^', '**')
        expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
        expr = re.sub(r'(\d)(\()', r'\1*\2', expr)
        expr = expr.replace('ln', 'log')  # <-- Add this if not present
        return expr
        
    def _create_function(self, function_str: str) -> FunctionData:
        x = sp.symbols('x')
        expr = sp.sympify(function_str)
        func = sp.lambdify(x, expr, "numpy")
        return FunctionData(func=func, expr=expr, x_symbol=x)
    
    def _safe_evaluate(self, func: Callable, x_val: float) -> Union[float, str]:
        try:
            value = float(func(x_val))
            if np.isposinf(value):
                return "∞"
            elif np.isneginf(value):
                return "-∞"
            elif np.isnan(value):
                return "undefined"
            return value
        except:
            try:
                epsilon_values = [1e-6, 1e-8, 1e-10]
                left_approaches = []
                right_approaches = []
                
                for eps in epsilon_values:
                    try:
                        left_approaches.append(func(x_val - eps))
                    except:
                        pass
                    try:
                        right_approaches.append(func(x_val + eps))
                    except:
                        pass
                
                if all(np.isposinf(v) for v in left_approaches + right_approaches if not np.isnan(v)):
                    return "∞"
                if all(np.isneginf(v) for v in left_approaches + right_approaches if not np.isnan(v)):
                    return "-∞"
                    
                return "undefined"
            except:
                return "undefined"

    def _find_critical_points(self, fn_data: FunctionData, x_min: float, x_max: float) -> List[float]:
        try:
            x = fn_data.x_symbol
            deriv = sp.diff(fn_data.expr, x)
            second_deriv = sp.diff(fn_data.expr, x, 2) 
            f_prime = sp.lambdify(x, deriv, "numpy")
            f_double = sp.lambdify(x, second_deriv, "numpy")
            
            critical_points = set()
            
            x_samples = np.linspace(x_min, x_max, 100)
            y_prime_samples = np.array([self._safe_evaluate_numeric(f_prime, x_val) for x_val in x_samples])
            sign_changes = np.where(np.diff(np.signbit(y_prime_samples)))[0]
            
            self._find_roots_at_sign_changes(f_prime, f_double, x_samples, sign_changes, 
                                           x_min, x_max, critical_points)
            
            self._try_additional_root_starts(f_prime, f_double, x_min, x_max, critical_points)
            
            return sorted(list(critical_points))
        except Exception as e:
            print(f"Error finding critical points: {str(e)}")
            return []
    
    def _safe_evaluate_numeric(self, func: Callable, x_val: float) -> float:
        try:
            result = float(func(x_val))
            return result if np.isfinite(result) else np.nan
        except:
            return np.nan
    
    def _find_roots_at_sign_changes(self, f_prime: Callable, f_double: Callable, 
                                  x_samples: np.ndarray, sign_changes: np.ndarray,
                                  x_min: float, x_max: float, results: set):
        for i in sign_changes:
            left, right = x_samples[i], x_samples[i + 1]
            x0 = (left + right) / 2  
            
            try:
                result = optimize.newton(f_prime, x0, fprime=f_double, maxiter=50, tol=1e-10)   
                if x_min <= result <= x_max and abs(self._safe_evaluate_numeric(f_prime, result)) < 1e-8:
                    results.add(round(result, 10))  
                    continue
            except:
                pass
            
            try:
                result = optimize.root_scalar(f_prime, bracket=[left, right])
                if result.converged:
                    results.add(round(result.root, 10))
            except:
                pass
    
    def _try_additional_root_starts(self, f_prime: Callable, f_double: Callable, 
                                  x_min: float, x_max: float, results: set):
        additional_starts = np.linspace(x_min, x_max, 10)
        for x0 in additional_starts:
            try:
                result = optimize.newton(f_prime, x0, fprime=f_double, maxiter=50, tol=1e-10)
                if x_min <= result <= x_max and abs(self._safe_evaluate_numeric(f_prime, result)) < 1e-8:
                    results.add(round(result, 10))
            except:
                pass

    def _find_inflection_points(self, fn_data: FunctionData, x_min: float, x_max: float) -> List[float]:
        try:
            x = fn_data.x_symbol
            second_deriv = sp.diff(fn_data.expr, x, 2)
            f_double_prime = sp.lambdify(x, second_deriv, "numpy")
            
            inflection_points = set()
            
            x_samples = np.linspace(x_min, x_max, 100)
            y_double_prime_samples = np.array([self._safe_evaluate_numeric(f_double_prime, x_val) for x_val in x_samples])
            sign_changes = np.where(np.diff(np.signbit(y_double_prime_samples)))[0]
            
            for i in sign_changes:
                left, right = x_samples[i], x_samples[i + 1]
                try:
                    result = optimize.root_scalar(f_double_prime, bracket=[left, right])
                    if result.converged:
                        inflection_points.add(round(result.root, 10))
                except:
                    pass
            
            return sorted(list(inflection_points))
        except Exception as e:
            print(f"Error finding inflection points: {str(e)}")
            return []

    def _detect_asymptotes(self, fn_data: FunctionData, x_min: float, x_max: float) -> List[float]:
        try:
            x_test = np.linspace(x_min, x_max, 500)
            y_test = np.array([self._safe_evaluate_numeric(fn_data.func, x_val) for x_val in x_test])
            
            y_diff = np.abs(np.diff(y_test))
            valid_diffs = y_diff[np.isfinite(y_diff)]
            
            if len(valid_diffs) == 0:
                return []
                
            threshold = np.nanmean(valid_diffs) + 5 * np.nanstd(valid_diffs)
            potential_asymptotes = np.where(y_diff > threshold)[0]
            
            nan_transitions = np.where(np.diff(np.isnan(y_test)))[0]
            potential_asymptotes = np.unique(np.concatenate([potential_asymptotes, nan_transitions]))
            
            asymptotes = []
            for idx in potential_asymptotes:
                x_value = (x_test[idx] + x_test[idx + 1]) / 2
                asymptotes.append(round(x_value, 10))
            
            filtered_asymptotes = []
            for asym in asymptotes:
                if not any(abs(asym - existing) < 1e-8 for existing in filtered_asymptotes):
                    filtered_asymptotes.append(asym)
            
            return filtered_asymptotes
        except Exception as e:
            print(f"Error detecting asymptotes: {str(e)}")
            return []

    def _create_variation_table(self, fn_data: FunctionData, x_min: float, x_max: float,
                          critical_points: List[float], asymptotes: List[float]) -> Dict[str, List]:
        try:
            x = fn_data.x_symbol
            first_deriv = sp.diff(fn_data.expr, x)
            second_deriv = sp.diff(fn_data.expr, x, 2)
            f_prime = sp.lambdify(x, first_deriv, "numpy")
            f_double_prime = sp.lambdify(x, second_deriv, "numpy")

            # --- FIX: Remove near-duplicate points ---
            raw_points = [x_min] + critical_points + asymptotes + [x_max]
            raw_points = [round(p, 10) for p in raw_points]
            raw_points.sort()
            all_points = []
            for p in raw_points:
                if not all_points or abs(p - all_points[-1]) > 1e-8:
                    all_points.append(p)
            # --- END FIX ---

            variation_table = {
                "intervals": [],
                "values": [],
                "directions": [],
                "firstDerivativeSign": [],
                "secondDerivativeSign": []
            }
            added_intervals = set()  # <-- Track intervals as tuples

            for i in range(len(all_points) - 1):
                start = round(all_points[i], 10)
                end = round(all_points[i+1], 10)

                if start in asymptotes or end in asymptotes or abs(end - start) < 1e-8:
                    continue

                interval_tuple = (start, end)
                if interval_tuple in added_intervals:
                    continue
                added_intervals.add(interval_tuple)

                mid_point = (start + end) / 2

                first_deriv_value = self._safe_evaluate_numeric(f_prime, mid_point)
                if np.isnan(first_deriv_value):
                    test_points = np.linspace(start, end, 5)
                    test_values = [self._safe_evaluate_numeric(fn_data.func, p) for p in test_points]
                    valid_values = [v for v in test_values if np.isfinite(v)]

                    if len(valid_values) >= 2:
                        diffs = np.diff(valid_values)
                        direction = "increasing" if np.mean(diffs) > 0 else "decreasing"
                        first_sign = "+" if direction == "increasing" else "-"
                    else:
                        direction = "undefined"
                        first_sign = "undefined"
                else:
                    direction = "increasing" if first_deriv_value > 0 else "decreasing"
                    first_sign = "+" if first_deriv_value > 0 else "-"

                second_deriv_value = self._safe_evaluate_numeric(f_double_prime, mid_point)
                if np.isnan(second_deriv_value):
                    try:
                        test_points = np.linspace(start, end, 5)
                        test_values = [self._safe_evaluate_numeric(f_prime, p) for p in test_points]
                        valid_values = [v for v in test_values if np.isfinite(v)]

                        if len(valid_values) >= 2:
                            diffs = np.diff(valid_values)
                            second_sign = "+" if np.mean(diffs) > 0 else "-"
                        else:
                            second_sign = "undefined"
                    except:
                        second_sign = "undefined"
                else:
                    second_sign = "+" if second_deriv_value > 0 else "-"

                start_value = self._safe_evaluate(fn_data.func, start)
                end_value = self._safe_evaluate(fn_data.func, end)

                variation_table["intervals"].append([start, end])
                variation_table["values"].append([start_value, end_value])
                variation_table["directions"].append(direction)
                variation_table["firstDerivativeSign"].append(first_sign)
                variation_table["secondDerivativeSign"].append(second_sign)
            
            # --- For asymptotes, also check for duplicates ---
            for asymptote in asymptotes:
                if asymptote <= x_min or asymptote >= x_max:
                    continue

                for i, point in enumerate(all_points):
                    if point == asymptote and i > 0 and i < len(all_points) - 1:
                        left_point = round(all_points[i-1], 10)
                        right_point = round(all_points[i+1], 10)

                        # Left interval
                        if abs(asymptote - left_point) > 1e-8:
                            interval_tuple = (left_point, asymptote)
                            if interval_tuple not in added_intervals:
                                added_intervals.add(interval_tuple)
                                mid_left = (left_point + asymptote * 3) / 4

                                first_deriv_value = self._safe_evaluate_numeric(f_prime, mid_left)
                                if np.isnan(first_deriv_value):
                                    left_dir = "undefined"
                                    first_sign = "undefined"
                                else:
                                    left_dir = "increasing" if first_deriv_value > 0 else "decreasing"
                                    first_sign = "+" if first_deriv_value > 0 else "-"

                                second_deriv_value = self._safe_evaluate_numeric(f_double_prime, mid_left)
                                second_sign = "+" if second_deriv_value > 0 else "-" if np.isfinite(second_deriv_value) else "undefined"

                                left_value = self._safe_evaluate(fn_data.func, left_point)
                                right_limit = self._safe_evaluate(fn_data.func, asymptote - 1e-8)

                                variation_table["intervals"].append([left_point, asymptote])
                                variation_table["values"].append([left_value, right_limit])
                                variation_table["directions"].append(left_dir)
                                variation_table["firstDerivativeSign"].append(first_sign)
                                variation_table["secondDerivativeSign"].append(second_sign)

                        # Right interval
                        if abs(right_point - asymptote) > 1e-8:
                            interval_tuple = (asymptote, right_point)
                            if interval_tuple not in added_intervals:
                                added_intervals.add(interval_tuple)
                                mid_right = (asymptote * 1 + right_point * 3) / 4

                                first_deriv_value = self._safe_evaluate_numeric(f_prime, mid_right)
                                if np.isnan(first_deriv_value):
                                    right_dir = "undefined"
                                    first_sign = "undefined"
                                else:
                                    right_dir = "increasing" if first_deriv_value > 0 else "decreasing"
                                    first_sign = "+" if first_deriv_value > 0 else "-"

                                second_deriv_value = self._safe_evaluate_numeric(f_double_prime, mid_right)
                                second_sign = "+" if second_deriv_value > 0 else "-" if np.isfinite(second_deriv_value) else "undefined"

                                left_limit = self._safe_evaluate(fn_data.func, asymptote + 1e-8)
                                right_value = self._safe_evaluate(fn_data.func, right_point)

                                variation_table["intervals"].append([asymptote, right_point])
                                variation_table["values"].append([left_limit, right_value])
                                variation_table["directions"].append(right_dir)
                                variation_table["firstDerivativeSign"].append(first_sign)
                                variation_table["secondDerivativeSign"].append(second_sign)
            
            return variation_table
        
        except Exception as e:
            print(f"Error creating variation table: {str(e)}")
            return {"intervals": [], "values": [], "directions": [], 
                   "firstDerivativeSign": [], "secondDerivativeSign": []}

    def adaptive_sampling(self, function_str: str, x_min: float, x_max: float, 
                        precision: int = 100, max_points: int = 3000) -> Tuple[np.ndarray, np.ndarray, list, list]:
        try:
            fn_data = self._create_function(function_str)
            
            critical_points = self._find_critical_points(fn_data, x_min, x_max)
            inflection_points = self._find_inflection_points(fn_data, x_min, x_max)
            asymptotes = self._detect_asymptotes(fn_data, x_min, x_max)

            critical_data_points = []
            inflection_data_points = []
            
            for point in critical_points:
                if x_min <= point <= x_max:
                    y_value = self._safe_evaluate_numeric(fn_data.func, point)
                    if np.isfinite(y_value):
                        critical_data_points.append([point, y_value])
                    
            for point in inflection_points:
                if x_min <= point <= x_max:
                    y_value = self._safe_evaluate_numeric(fn_data.func, point)
                    if np.isfinite(y_value):
                        inflection_data_points.append([point, y_value])
            
            special_points = critical_points + inflection_points
            
            for asym in asymptotes:
                delta = (x_max - x_min) / 500
                special_points.extend([asym - delta, asym + delta])
            
            x_values = np.sort(np.append(np.linspace(x_min, x_max, precision), special_points))
            y_values = np.array([self._safe_evaluate_numeric(fn_data.func, x_val) for x_val in x_values])
            
            if len(x_values) > max_points:
                x_values, y_values = self._downsample_points(x_values, y_values, special_points, max_points)
            
            x_values, y_values = self._add_intermediate_points(x_values, y_values, fn_data.func, y_values)
            
            return np.array(x_values), np.array(y_values), critical_data_points, inflection_data_points
        
        except Exception as e:
            print(f"Error in adaptive sampling: {str(e)}")
            return np.array([]), np.array([]), [], []
    
    def _downsample_points(self, x_values: np.ndarray, y_values: np.ndarray, 
                          special_points: List[float], max_points: int) -> Tuple[np.ndarray, np.ndarray]:
        keep_mask = np.zeros(len(x_values), dtype=bool)
        
        for point in special_points:
            idx = np.abs(x_values - point).argmin()
            keep_mask[idx] = True
        
        keep_mask[0] = keep_mask[-1] = True
        
        remaining_indices = np.where(~keep_mask)[0]
        if len(remaining_indices) > 0:
            importance = np.zeros(len(remaining_indices))
            
            for i, idx in enumerate(remaining_indices):
                if idx > 0 and idx < len(x_values) - 1:
                    left_slope = (y_values[idx] - y_values[idx-1]) / max(x_values[idx] - x_values[idx-1], 1e-10)
                    right_slope = (y_values[idx+1] - y_values[idx]) / max(x_values[idx+1] - x_values[idx], 1e-10)
                    if np.isfinite(left_slope) and np.isfinite(right_slope):
                        importance[i] = abs(right_slope - left_slope)
            
            important_indices = remaining_indices[np.argsort(importance)[::-1]]
            points_to_add = min(len(important_indices), max_points - np.sum(keep_mask))
            keep_mask[important_indices[:points_to_add]] = True
        
        return x_values[keep_mask], y_values[keep_mask]
    
    def _add_intermediate_points(self, x_values: np.ndarray, y_values: np.ndarray, 
                               func: Callable, all_y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        std = np.nanstd(all_y)
        threshold = 10 * std if not np.isnan(std) else 10
        
        final_x, final_y = [], []
        for i in range(len(x_values) - 1):
            final_x.append(x_values[i])
            final_y.append(y_values[i])
            
            if (np.isfinite(y_values[i]) and np.isfinite(y_values[i+1]) and 
                abs(y_values[i+1] - y_values[i]) > threshold):
                intermediate_x = np.linspace(x_values[i], x_values[i+1], 5)[1:-1]
                intermediate_y = np.array([self._safe_evaluate_numeric(func, x_val) for x_val in intermediate_x])
                
                final_x.extend(intermediate_x)
                final_y.extend(intermediate_y)
        
        final_x.append(x_values[-1])
        final_y.append(y_values[-1])
        
        return np.array(final_x), np.array(final_y)

    def generate_plot_data(self, function: str, lower_bound: float, upper_bound: float, 
                         precision: int, max_points: int, isFirstPlot : bool) -> Dict[str, Any]:
        try:
            lower = lower_bound if lower_bound is not None else -10
            upper = upper_bound if upper_bound is not None else 10
            if lower >= upper:
                raise ValueError("Lower bound must be less than upper bound.")
            
            function = self._convert_to_python_expr(function)
            
            fn_data = self._create_function(function)
            
            x, y, critical_points, inflection_points = self.adaptive_sampling(
                function, 
                lower,
                upper,
                precision=precision,
                max_points=max_points
            )
            
            asymptotes = self._detect_asymptotes(fn_data, lower, upper)
            
            critical_x_values = [point[0] for point in critical_points]
            variation_table = self._create_variation_table(
                fn_data,
                lower,
                upper,
                critical_x_values,
                asymptotes
            )
            
            mask = np.isfinite(y)
            x = x[mask]
            y = y[mask]
            
            unique_mask = np.append(True, np.diff(x) > 1e-10)
            x = x[unique_mask]
            y = y[unique_mask]

            # --- If all values overflow, try plotting from -10 to 10 ---
            if len(x) == 0 or len(y) == 0:
                if lower != -10 or upper != 10:
                    # Try again with default interval
                    return self.generate_plot_data(function, -10, 10, precision, max_points, isFirstPlot)
                else:
                    raise Exception("All values overflowed or are invalid for the selected interval and for [-10, 10]. Try a different function.")
            # ----------------------------------------------------------

            data = {'x': x.tolist(), 'y': y.tolist()}
            packed_data = msgpack.packb(data)
            compressed_data = zlib.compress(packed_data)
            
            return {
                "data": base64.b64encode(compressed_data).decode('utf-8'),
                "pointsCount": len(x),
                "criticalPoints": critical_points,
                "inflectionPoints": inflection_points,
                "variationTable": variation_table,
                "isFirstPlot": isFirstPlot
            }
        
        except Exception as e:
            raise Exception(f"Error processing function '{function}': {str(e)}")



