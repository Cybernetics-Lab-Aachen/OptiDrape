#ifndef OPTIDRAPE_MAIN_H
#define OPTIDRAPE_MAIN_H

#include <QMainWindow>

namespace Ui {
class OptiDrape_Main;
}

class OptiDrape_Main : public QMainWindow
{
    Q_OBJECT

public:
    explicit OptiDrape_Main(QWidget *parent = 0);
    ~OptiDrape_Main();

private:
    Ui::OptiDrape_Main *ui;
};

#endif // OPTIDRAPE_MAIN_H
