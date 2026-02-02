import pytest
from schema import Transaction

def test_transaction_schema():
    tx = Transaction(
        V1=0.1, V2=0.1, V3=0.1, V4=0.1, V5=0.1,
        V6=0.1, V7=0.1, V8=0.1, V9=0.1, V10=0.1,
        V11=0.1, V12=0.1, V13=0.1, V14=0.1, V15=0.1,
        V16=0.1, V17=0.1, V18=0.1, V19=0.1, V20=0.1,
        V21=0.1, V22=0.1, V23=0.1, V24=0.1, V25=0.1,
        V26=0.1, V27=0.1, V28=0.1, Amount=100.0
    )
    # Check Amount field
    assert tx.Amount == 100.0
    # Check one other field as example
    assert tx.V1 == 0.1
