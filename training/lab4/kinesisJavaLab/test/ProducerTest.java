
// Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

import static org.junit.Assert.*;
import org.junit.Test;

import java.util.concurrent.TimeUnit;

public class ProducerTest {
    @Test
    public void testMain() throws Exception {
        SensorReadingsProducer.main(new String[0]);

        long endTime = System.currentTimeMillis() + TimeUnit.SECONDS.toMillis(10);

        while (System.currentTimeMillis() < endTime
            && SensorReadingsProducer.getSensorReadingsProducer().getSuccessCounter() < SensorReadingsProducer.TOTAL_NUM_EVENTS) {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException ie) {
            }
        }
        
        int successCounter = SensorReadingsProducer.getSensorReadingsProducer().getSuccessCounter();
        String msg = String.format("Failed to add records to stream. Number of records added: %d; Number of records expected: %d", successCounter,
                SensorReadingsProducer.TOTAL_NUM_EVENTS);

        
        assertEquals(msg, SensorReadingsProducer.TOTAL_NUM_EVENTS, successCounter);
    }
}
