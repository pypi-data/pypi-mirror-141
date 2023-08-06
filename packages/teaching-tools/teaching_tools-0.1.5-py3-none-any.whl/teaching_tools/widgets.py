import itertools
from string import Template

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Math, display
from matplotlib.patches import Rectangle
from sklearn.exceptions import NotFittedError
from sklearn.metrics import confusion_matrix
from sklearn.utils.validation import check_is_fitted


class ConfusionMatrixWidget:
    def __init__(self, model, X_test, y_test):
        self.model = model
        self.X_test = X_test
        self.y_test = y_test
        self._y_pred = None
        self._cnf_matrix = None

        plt.rcParams.update({"font.size": 25})

    def __repr__(self):
        class_name = type(self).__name__
        model = type(self.model).__name__
        X_test = type(self.X_test).__name__
        y_test = type(self.y_test).__name__
        return "{}(model={}, X_test={}, y_test={})".format(
            class_name, model, X_test, y_test
        )

    def __str__(self):
        class_name = type(self).__name__
        model = type(self.model).__name__
        X_test = type(self.X_test).__name__
        y_test = type(self.y_test).__name__
        return "{}(model={}, X_test={}, y_test={})".format(
            class_name, model, X_test, y_test
        )

    def __generate_predictions(self, thresh=0.5):
        try:
            check_is_fitted(self.model)
        except NotFittedError:
            self.model.fit(self.X_test, self.y_test)

        try:
            pred_proba = self.model.predict_proba(self.X_test)[:, -1]
            self._y_pred = pred_proba > thresh
        except AttributeError:
            raise AttributeError(
                "Widget only works with models that have a `predict_proba` method."
            )

    def __generate_cnf(self, thresh=0.5, rot90=False):
        self.__generate_predictions(thresh)
        _cnf_matrix = confusion_matrix(self.y_test, self._y_pred)
        if rot90:
            _cnf_matrix = np.rot90(_cnf_matrix, axes=(1, 0))
        self._cnf_matrix = _cnf_matrix

    def __acc_score_equation(self, w):
        with self.accuracy_plt:
            self.accuracy_plt.clear_output(wait=True)
            self.__generate_cnf(self.t_widget.value)
            tn, fp, fn, tp = self._cnf_matrix.ravel()
            score = round(sum([tp + tn]) / sum([tp, fp, fn, tn]), 2)
            s = r"""
                \text{Accuracy} = \dfrac{
                    \color{purple}{$TP}
                    + \color{orange}{$TN}
                }{
                    \color{purple}{$TP}
                    + \color{blue}{$FN}
                    + \color{orange}{$TN}
                    + \color{red}{$FP}
                } = $SCORE
            """
            temp = Template(s).substitute(
                TP=tp, FP=fp, TN=tn, FN=fn, SCORE=score
            )
            display(Math(temp))

    def __precision_score_equation(self, w):
        with self.precision_plt:
            self.precision_plt.clear_output(wait=True)
            self.__generate_cnf(self.t_widget.value)
            _, fp, _, tp = self._cnf_matrix.ravel()
            score = round(tp / (tp + fp), 2)
            s = r"""
                \text{Precision} = \dfrac{
                    \color{purple}{$TP}
                }{
                    \color{purple}{$TP}
                    + \color{red}{$FP}
                } = $SCORE
            """
            temp = Template(s).substitute(TP=tp, FP=fp, SCORE=score)
            display(Math(temp))

    def __recall_score_equation(self, w):
        with self.recall_plt:
            self.recall_plt.clear_output(wait=True)
            self.__generate_cnf(self.t_widget.value)
            _, _, fn, tp = self._cnf_matrix.ravel()
            score = round(tp / (tp + fn), 2)
            s = r"""
                \text{Recall} = \dfrac{
                    \color{purple}{$TP}
                }{
                    \color{purple}{$TP}
                    + \color{blue}{$FN}
                } = $SCORE
            """
            temp = Template(s).substitute(TP=tp, FN=fn, SCORE=score)
            display(Math(temp))

    def __cnf_matrix(self, w):
        # https://github.com/jupyter-widgets/ipywidgets/issues/1919
        with self.cnf_plot:
            # Clear output
            self.cnf_plot.clear_output(wait=True)

            # Create confusion matrix
            self.__generate_cnf(self.t_widget.value, rot90=True)

            # Set colors
            color_matrix = np.array([["blue", "orange"], ["purple", "red"]])

            # Create fig
            fig = plt.figure(figsize=(10, 10))  # noQA F841
            ax = plt.subplot(111, aspect="equal")

            # Create plot
            for i, j in itertools.product(
                range(self._cnf_matrix.shape[0]),
                range(self._cnf_matrix.shape[1]),
            ):
                # Add patch
                sq = Rectangle(
                    xy=(i, j),
                    width=1,
                    height=1,
                    fc=color_matrix[i, j],
                    alpha=0.5,
                    ec="black",
                    label="Label",
                )
                ax.add_patch(sq)

                # Calculate label position
                rx, ry = sq.get_xy()
                cx = rx + sq.get_width() / 2.0
                cy = ry + sq.get_height() / 2.0

                # Add labels
                ax.annotate(
                    self._cnf_matrix[i, j],
                    (cx, cy),
                    color="black",
                    ha="center",
                    va="center",
                )
            ax.autoscale_view()
            ax.set_frame_on(False)
            plt.xticks(ticks=(0.5, 1.5), labels=[False, True])
            plt.yticks(ticks=(0.5, 1.5), labels=[True, False])
            plt.xlabel("Predicted label")
            plt.ylabel("True label")
            plt.show()

    def show(self):
        # Create widgets
        self.cnf_plot = widgets.Output(
            layout=widgets.Layout(height="300px", width="300px")
        )
        self.accuracy_plt = widgets.Output(
            layout=widgets.Layout(height="80px", width="400px")
        )
        self.precision_plt = widgets.Output(
            layout=widgets.Layout(height="80px", width="400px")
        )
        self.recall_plt = widgets.Output(
            layout=widgets.Layout(height="80px", width="400px")
        )
        self.t_widget = widgets.FloatSlider(
            value=0.5, min=0.0, max=1, step=0.1, description="Threshold:"
        )

        # Run helper funtions
        self.__cnf_matrix([])
        self.__acc_score_equation([])
        self.__precision_score_equation([])
        self.__recall_score_equation([])

        # Attach threshold widget to helper functions
        self.t_widget.observe(self.__cnf_matrix)
        self.t_widget.observe(self.__acc_score_equation)
        self.t_widget.observe(self.__precision_score_equation)
        self.t_widget.observe(self.__recall_score_equation)

        equations = widgets.VBox(
            [self.accuracy_plt, self.precision_plt, self.recall_plt]
        )
        hbx = widgets.HBox([self.cnf_plot, equations])
        display(self.t_widget, hbx)
