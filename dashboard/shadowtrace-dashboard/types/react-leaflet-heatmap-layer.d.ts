declare module "react-leaflet-heatmap-layer" {
  import { Component } from "react";
  import { LayerProps } from "react-leaflet";

  interface HeatmapLayerProps extends LayerProps {
    points: [number, number, number][];
    longitudeExtractor: (p: [number, number, number]) => number;
    latitudeExtractor: (p: [number, number, number]) => number;
    intensityExtractor: (p: [number, number, number]) => number;
    fitBoundsOnLoad?: boolean;
    fitBoundsOnUpdate?: boolean;
  }

  export default class HeatmapLayer extends Component<HeatmapLayerProps> {}
}
