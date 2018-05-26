#include "optidrape_main.h"
#include "ui_optidrape_main.h"

OptiDrape_Main::OptiDrape_Main(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::OptiDrape_Main)
{
    ui->setupUi(this);
}

OptiDrape_Main::~OptiDrape_Main()
{
    delete ui;
}
